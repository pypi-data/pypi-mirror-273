import torch
from jaxtyping import Float, Int
from torch import Tensor, nn
from typing import Union, Optional, Tuple
import trimesh

from pytorch3d.renderer import (
    PerspectiveCameras,
    MeshRasterizer,
    RasterizationSettings,
    Textures,
    PointsRasterizationSettings,
    PointsRasterizer,
    PointsRenderer,
    NormWeightedCompositor
)
from pytorch3d.structures import Meshes, Pointclouds

from pytorch3d.renderer.blending import (
    BlendParams,
)
from pytorch3d.renderer.lighting import PointLights
from pytorch3d.renderer.materials import Materials
from typing import Optional, Tuple, Union

import torch
import torch.nn as nn


class TextureShader(nn.Module):
    """
    Basic shader which just returns the texels.
    """

    def __init__(self, device="cpu", cameras=None, lights=None, materials=None, blend_params=None):
        super().__init__()
        self.lights = lights if lights is not None else PointLights(device=device)
        self.materials = materials if materials is not None else Materials(device=device)
        self.cameras = cameras
        self.blend_params = blend_params if blend_params is not None else BlendParams()

    def forward(self, fragments, meshes, **kwargs) -> torch.Tensor:
        texels = meshes.sample_textures(fragments)
        return texels[:, :, :, 0, :]

class MeshRendererWithDepth(torch.nn.Module):
    def __init__(self, rasterizer, shader):
        super().__init__()
        self.rasterizer = rasterizer
        self.shader = shader

    def forward(self, meshes_world, **kwargs) -> torch.Tensor:
        fragments = self.rasterizer(meshes_world, **kwargs)
        images = self.shader(fragments, meshes_world, **kwargs)
        return images, fragments.zbuf, fragments.pix_to_face

def get_face_max_edge_distances(
    vertices: Float[Tensor, "bs 3 H W"], faces: Float[Tensor, "bs 3 H W"]
) -> Float[Tensor, "bs H W"]:
    """Get the face normals."""
    face_pos = vertices.permute(0, 2, 3, 1).reshape(-1, 3)[faces]
    ab = face_pos[:, 1] - face_pos[:, 0]
    ab_dist = torch.norm(ab, dim=-1, keepdim=True)
    ac = face_pos[:, 2] - face_pos[:, 0]
    ac_dist = torch.norm(ac, dim=-1, keepdim=True)
    bc = face_pos[:, 2] - face_pos[:, 1]
    bc_dist = torch.norm(bc, dim=-1, keepdim=True)
    dist = torch.cat([ab_dist, ac_dist, bc_dist], dim=-1).permute(0, 3, 1, 2)
    dist = torch.max(dist, dim=1, keepdim=False).values
    return dist

def get_mesh(
    images: Float[Tensor, "bs 3 H W"],
    vertices: Float[Tensor, "bs 3 H W"],
    masks: Optional[Float[Tensor, "bs H W"]] = None,
    distance_threshold: Optional[float] = None,
    c2w: Optional[Float[Tensor, "3 4"]] = None,
) -> Tuple[Float[Tensor, "N 3"], Float[Tensor, "N 3"], Float[Tensor, "M 3"]]:
    """Returns a mesh from a perspective image.
    Fov is in radians.
    Assumes Blender camera conventions.
        - x right
        - y up
        - z back
    """

    device = images.device
    bs, _, H, W = images.shape

    vertex_ids = torch.arange(bs * H * W).reshape(bs, 1, H, W).to(device)
    vertex_00 = vertex_ids[:, :, : H - 1, : W - 1]
    vertex_01 = vertex_00 + 1
    vertex_10 = vertex_00 + W
    vertex_11 = vertex_00 + W + 1

    # faces
    faces_ul = torch.cat([vertex_00, vertex_10, vertex_01], dim=1)
    faces_lr = torch.cat([vertex_10, vertex_11, vertex_01], dim=1)

    mask_ul = torch.ones_like(faces_ul[:, 0, :, :]) == 1.0
    mask_lr = torch.ones_like(faces_lr[:, 0, :, :]) == 1.0

    if masks is not None:
        mask_ul = mask_ul & (masks[:, :-1, :-1] != 0.0)
        mask_lr = mask_lr & (masks[:, 1:, 1:] != 0.0)

    if distance_threshold:
        faces_max_edge_dist_ul = get_face_max_edge_distances(vertices, faces_ul)
        faces_max_edge_dist_lr = get_face_max_edge_distances(vertices, faces_lr)
        mask_ul &= faces_max_edge_dist_ul <= distance_threshold
        mask_lr &= faces_max_edge_dist_lr <= distance_threshold

    faces = torch.cat([faces_ul.permute(0, 2, 3, 1), faces_lr.permute(0, 2, 3, 1)]).reshape(-1, 3)
    faces_mask = torch.cat([mask_ul, mask_lr]).reshape(-1)

    vertices = vertices.permute(0, 2, 3, 1).reshape(-1, 3)
    vertex_colors = images.clone().permute(0, 2, 3, 1).reshape(-1, 3)

    if c2w is not None:
        verticesh = torch.cat([vertices, torch.ones_like(vertices[:, :1])], dim=-1)
        vertices = torch.matmul(c2w, verticesh.permute(1, 0)).permute(1, 0)

    return vertices, vertex_colors, faces, faces_mask

def save_mesh(
    vertices: Float[Tensor, "N 3"],
    vertex_colors: Float[Tensor, "N 3"],
    faces: Float[Tensor, "M 3"],
    filename="mesh.ply",
):
    mesh = trimesh.Trimesh(
        vertices=vertices.detach().cpu().numpy(),
        faces=faces.detach().cpu().numpy(),
        vertex_colors=vertex_colors.detach().cpu().numpy(),
    )
    mesh.remove_unreferenced_vertices()
    mesh.export(filename)
    return mesh

def c2wh_from_c2w(c2w):
    c2wh = torch.cat([c2w, torch.zeros_like(c2w[:1])])
    c2wh[-1, -1] = 1
    return c2wh

def get_transformed_vertices(vertices: Float[Tensor, "N 3"], c2w=None, device=None):
    if c2w is None:
        return vertices

    # compute world to camera transformation
    c2wh = c2wh_from_c2w(c2w).to(device)
    w2ch = torch.inverse(c2wh)

    # apply the transformation
    transformed_vertices = torch.cat([vertices, torch.ones_like(vertices[:, :1])], dim=-1)
    transformed_vertices = (w2ch @ transformed_vertices.permute(1, 0)).permute(1, 0)
    transformed_vertices = transformed_vertices[:, :3]
    return transformed_vertices

def render_mesh(
    vertices: Float[Tensor, "N 3"],
    colors: Union[Float[Tensor, "N 3"], None],
    faces: Float[Tensor, "M 3"],
    focal_length: Float[Tensor, "2"],
    principal_point: Float[Tensor, "2"],
    image_size: int,
    c2w: Float[Tensor, "3 4"],
    faces_per_pixel=1,
    textures: Optional[Textures] = None,
    cull_backfaces: bool = False,
    device=None,
):
    """
    Projects a mesh into a camera. We only render front-facing triangles ordered in an anti-clockwise fashion.
    """
    if device is None:
        device = vertices.device

    assert device != "cpu", "Rendering with cpu will be slow!"

    transformed_vertices = get_transformed_vertices(vertices, c2w=c2w, device=device)

    if textures is None:
        assert colors is not None
        meshes = Meshes(
            verts=[transformed_vertices],
            faces=[faces],
            textures=Textures(verts_rgb=colors.unsqueeze(0)),
        )
    else:
        meshes = Meshes(verts=[transformed_vertices], faces=[faces], textures=textures)

    R = torch.eye(3).unsqueeze(0)
    T = torch.zeros(3).unsqueeze(0)

    # rotate 180 degrees around Y axis
    m = torch.tensor([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]).unsqueeze(0).float()
    R = torch.bmm(m, R)

    fl = focal_length.unsqueeze(0)
    pp = principal_point.unsqueeze(0)
    image_size_ = torch.tensor(image_size).to(fl).unsqueeze(0)
    cameras = PerspectiveCameras(focal_length=fl, principal_point=pp, R=R, T=T, device=device, in_ndc=False, image_size=image_size_)

    raster_settings = RasterizationSettings(
        image_size=image_size,
        blur_radius=0.0,
        faces_per_pixel=faces_per_pixel,
        cull_backfaces=cull_backfaces,
    )
    renderer = MeshRendererWithDepth(
        rasterizer=MeshRasterizer(cameras=cameras, raster_settings=raster_settings),
        shader=TextureShader(device=device, cameras=cameras),
    )

    images, depths, pix_to_face = renderer(meshes)
    image = images[0, :, :, :3]
    depth = depths[0, :, :, 0]

    return image, depth, pix_to_face[0]

def render_point_cloud(
    vertices: Float[Tensor, "N 3"],
    colors: Union[Float[Tensor, "N 3"], None],
    focal_length: Float[Tensor, "2"],
    principal_point: Float[Tensor, "2"],
    image_size: int,
    c2w: Float[Tensor, "3 4"],
    point_radius: float = 0.02,
    device=None,
):
    """
    Projects a mesh into a camera. We only render front-facing triangles ordered in an anti-clockwise fashion.
    """
    if device is None:
        device = vertices.device

    assert device != "cpu", "Rendering with cpu will be slow!"

    transformed_vertices = get_transformed_vertices(vertices, c2w=c2w, device=device)

    point_cloud = Pointclouds(points=[transformed_vertices], features=[colors])

    R = torch.eye(3).unsqueeze(0)
    T = torch.zeros(3).unsqueeze(0)

    # rotate 180 degrees around Y axis
    m = torch.tensor([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]).unsqueeze(0).float()
    R = torch.bmm(m, R)

    fl = focal_length.unsqueeze(0)
    pp = principal_point.unsqueeze(0)
    image_size_ = torch.tensor(image_size).to(fl).unsqueeze(0)
    cameras = PerspectiveCameras(focal_length=fl, principal_point=pp, R=R, T=T, device=device, in_ndc=False, image_size=image_size_)

    raster_settings = PointsRasterizationSettings(
        image_size=image_size, 
        radius = point_radius,
        points_per_pixel = 10
    )
    renderer = PointsRenderer(
        rasterizer=PointsRasterizer(cameras=cameras, raster_settings=raster_settings),
        compositor=NormWeightedCompositor(background_color=(1,1,1))
    )

    images = renderer(point_cloud)
    image = images[0, :, :, :3]

    return image