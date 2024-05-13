import cv2
import pytorch3d
from pytorch3d.structures import Meshes
from pytorch3d.renderer import (
    MeshRenderer,
    MeshRasterizer,
    TexturesUV,
    look_at_view_transform,
    OrthographicCameras,
    RasterizationSettings,
)
import torch
import torch.nn as nn

# from .arap import compute_energy as arap_loss
from scipy.spatial import Delaunay
from toon3d.utils.pytorch_arap.arap import ARAPMeshes, ARAP_from_meshes, compute_energy


def shi_tomasi(images, max_corners, min_distance=10, device="cuda:0"):
    """Finds corners in a batch of images"""
    batch_size, height, width = images.shape[:3]

    max_num_corners = 0
    corners_list = []
    for image in images:
        gray_img = cv2.cvtColor(image.cpu().numpy(), cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray_img, max_corners, 0.001, min_distance)

        max_num_corners = max(max_num_corners, len(corners))

        corners[..., 0] = (2 * corners[..., 0] / width) - 1
        corners[..., 1] = (2 * corners[..., 1] / height) - 1
        corners_list.append(corners[:, 0])

    corners = torch.zeros([len(images), max_num_corners, 2])
    masks = torch.zeros([len(images), max_num_corners], dtype=torch.bool)

    for bi in range(batch_size):
        corners[bi, : len(corners_list[bi])] = torch.from_numpy(corners_list[bi])
        masks[bi, : len(corners_list[bi])] = True

    return corners.to(device), masks.to(device)


def get_simplices(points, mask=None):
    """Returns a batch of simplices for the keypoints.
    Keypoints of shape [b, n, 2] as (x,y) coordinates in range [-1,1].
    """

    if mask is None:
        mask = torch.ones(len(points), dtype=torch.bool)

    tri = Delaunay(points[mask].detach().cpu().numpy(), qhull_options="QJ")
    simplices = torch.tensor(tri.simplices, device=points.device)
    masked_out_ndxs = torch.where(mask == False)[0]
    for ndx in masked_out_ndxs:
        simplices[simplices >= ndx] += 1

    return simplices


class WarpModel(nn.Module):
    """Images to be Warped"""

    def __init__(self, images, keypoints, keypoint_masks, device="cuda:0"):
        super().__init__()

        assert isinstance(images, list), "images must be a list. TODO: the code will need to be modified for this"

        self.images = images.to(device)
        self.n, self.height, self.width = images.shape[:3]

        self.keypoints = keypoints.to(device)
        self.keypoint_masks = keypoint_masks.to(device)
        self.produce_extra_points(min_distance=min(self.width, self.height) // 25)

        self.keypoints_list = [points[mask] for points, mask in zip(self.keypoints, self.keypoint_masks)]
        self.simplices = [get_simplices(keypoints) for keypoints in self.keypoints_list]

        self.device = device

        self.meshes = self.make_meshes()
        self.arap_meshes = ARAP_from_meshes(self.meshes)

        self.template_verts = self.meshes.verts_padded()
        self.deform_verts = torch.zeros(self.template_verts.shape, device=device, requires_grad=True)

        self.renderer = self.make_renderer()

    def produce_extra_points(self, min_distance, max_corners=1000):
        extra_points, extra_masks = shi_tomasi(self.images, max_corners, min_distance)

        # filter points too close to original points
        for i in range(self.n):
            kp1 = self.keypoints[i].clone()
            kp2 = extra_points[i].clone()

            kp1[..., 0] = (kp1[..., 0] + 1) / 2 * self.width
            kp1[..., 1] = (kp1[..., 1] + 1) / 2 * self.height

            kp2[..., 0] = (kp2[..., 0] + 1) / 2 * self.width
            kp2[..., 1] = (kp2[..., 1] + 1) / 2 * self.height

            dists = torch.sqrt(((kp1[:, None, :] - kp2[None, :, :]) ** 2).sum(-1))
            nearest_neighbors = dists.min(0)
            nn_mask = nearest_neighbors[0] > min_distance
            extra_masks[i] = torch.logical_and(extra_masks[i], nn_mask)

        # Filter if outside original range of points
        for i in range(self.n):
            points_x = self.keypoints[i][..., 0][self.keypoint_masks[i]]
            points_y = self.keypoints[i][..., 1][self.keypoint_masks[i]]

            extra_points_x = extra_points[i][..., 0]
            extra_points_y = extra_points[i][..., 1]

            high_width_mask = extra_points_x > torch.min(points_x)
            small_width_mask = extra_points_x < torch.max(points_x)
            width_mask = torch.logical_and(high_width_mask, small_width_mask)

            high_height_mask = extra_points_y > torch.min(points_y)
            small_height_mask = extra_points_y < torch.max(points_y)
            height_mask = torch.logical_and(high_height_mask, small_height_mask)

            outside_mask = torch.logical_and(height_mask, width_mask)
            extra_masks[i] = torch.logical_and(extra_masks[i], outside_mask)

        self.keypoints = torch.cat([self.keypoints, extra_points], 1)
        self.keypoint_masks = torch.cat([self.keypoint_masks, extra_masks], 1)

    def make_meshes(self):
        """Create Meshes from points"""
        flip = torch.tensor([1, -1]).to(self.device)
        ratio = self.width / self.height

        meshes_vertices = []
        for mesh_points in self.keypoints_list:
            mesh_vertices = torch.cat(
                [mesh_points * flip, torch.zeros(len(mesh_points))[..., None].to(self.device)], -1
            )
            if ratio > 1:
                mesh_vertices[..., 0] *= ratio
            elif ratio < 1:
                mesh_vertices[..., 1] *= ratio
            meshes_vertices.append(mesh_vertices)

        verts_uvs = [(points * flip + 1) / 2 for points in self.keypoints_list]

        # print(self.images.device, self.simplices[0].device, verts_uvs[0].device)
        meshes = Meshes(verts=meshes_vertices, faces=self.simplices).to(self.device)
        meshes.textures = TexturesUV(self.images, faces_uvs=self.simplices, verts_uvs=verts_uvs).to(self.device)
        return meshes

    def make_renderer(self):
        R, T = look_at_view_transform(-5, 0, 180)
        cameras = OrthographicCameras(device=self.device, R=R, T=T)

        raster_settings = RasterizationSettings(
            image_size=(self.height, self.width),
            blur_radius=0.0,
            faces_per_pixel=1,
        )

        class SimpleShader(nn.Module):
            """No Shade Shader"""

            def __init__(self):
                super().__init__()
                self.blend_params = pytorch3d.renderer.blending.BlendParams()

            def forward(self, fragments, meshes, **kwargs) -> torch.Tensor:
                """Returns no shade"""
                blend_params = kwargs.get("blend_params", self.blend_params)
                texels = meshes.sample_textures(fragments)
                images = pytorch3d.renderer.blending.hard_rgb_blend(texels, fragments, blend_params)
                return images  # (N, H, W, 3) RGBA image

        renderer = MeshRenderer(
            rasterizer=MeshRasterizer(cameras=cameras, raster_settings=raster_settings), shader=SimpleShader()
        )

        return renderer

    def forward(self, ndx):
        images = self.renderer(self.meshes.update_padded(self.template_verts + self.deform_verts))[ndx]
        arap_loss = compute_energy(
            self.arap_meshes, self.template_verts, self.template_verts + self.deform_verts, ndx, device=self.device
        ).abs()

        return images, arap_loss
