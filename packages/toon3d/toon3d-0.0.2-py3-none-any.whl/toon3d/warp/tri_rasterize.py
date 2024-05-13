import torch
import torch.nn as nn
from tqdm import tqdm

from pytorch3d.ops.interp_face_attrs import interpolate_face_attributes
from pytorch3d.renderer.blending import hard_rgb_blend, BlendParams
from pytorch3d.renderer.mesh.rasterize_meshes import _RasterizeFaceVerts
from pytorch3d.renderer.mesh.rasterizer import Fragments


def rasterize_face_verts(face_verts, im_size, faces_per_pixel):
        assert face_verts.shape[1] == 3 and face_verts.shape[2]
        face_verts[...,:2] = -face_verts[...,:2]
        mesh_to_face_first_idx = torch.tensor([0], device=face_verts.device)
        num_faces_per_mesh = torch.tensor([len(face_verts)], device=face_verts.device)
        clipped_faces_neighbor_idx = torch.full((len(face_verts),), -1, device=face_verts.device)
        assert len(im_size) == 2 
        blur_radius = 1e-10
        assert faces_per_pixel > 0
        bin_size = 0
        max_faces_per_bin = 1
        perspective_correct = False
        clip_barycentric_coords = False
        cull_backfaces = False

        pix_to_face, zbuf, barycentric_coords, dists = _RasterizeFaceVerts.apply(
            face_verts,
            mesh_to_face_first_idx,
            num_faces_per_mesh,
            clipped_faces_neighbor_idx,
            im_size,
            blur_radius,
            faces_per_pixel,
            bin_size,
            max_faces_per_bin,
            perspective_correct,
            clip_barycentric_coords,
            cull_backfaces,
        )

        fragments = Fragments(pix_to_face=pix_to_face, zbuf=zbuf, bary_coords=barycentric_coords, dists=dists)

        return fragments

def rasterize_constant_color(image, fragments, return_errors=False):
    pix_to_face = fragments.pix_to_face
    k = pix_to_face.shape[-1]
    batch_image = image.unsqueeze(-2).repeat(1, 1, 1, k, 1)

    valid_pxs = pix_to_face.flatten() != -1
    tri_counts = torch.bincount(pix_to_face.flatten()[valid_pxs])
    tri_color_sums = torch.stack(
        [
            torch.bincount(pix_to_face.flatten()[valid_pxs], batch_image[..., c].flatten()[valid_pxs])
            for c in range(3)
        ]
    )
    tri_color_means = (tri_color_sums / tri_counts).T
    tri_color_means = nn.functional.pad(tri_color_means, (0, 0, 0, 1), 'constant', 0)

    tri_rast = tri_color_means[pix_to_face]

    if return_errors:
        error = ((batch_image - tri_rast) ** 2).sum(-1) / 2
        tri_errors = torch.bincount(pix_to_face.flatten()[valid_pxs], error.flatten()[valid_pxs], minlength=len(tri_counts))

        return tri_rast, tri_counts, tri_errors
    
    return tri_rast


def sample_texture(textures, verts_uvs, fragments):
    """
    https://github.com/facebookresearch/pytorch3d/blob/main/pytorch3d/renderer/mesh/textures.py
    """
    pixel_uvs = interpolate_face_attributes(fragments.pix_to_face, fragments.bary_coords, verts_uvs)

    N, H_out, W_out, K = fragments.pix_to_face.shape
    N, H_in, W_in, C = textures.shape  # 3 for RGB

    # pixel_uvs: (N, H, W, K, 2) -> (N, K, H, W, 2) -> (NK, H, W, 2)
    pixel_uvs = pixel_uvs.permute(0, 3, 1, 2, 4).reshape(N * K, H_out, W_out, 2)

    # textures.map:
    #   (N, H, W, C) -> (N, C, H, W) -> (1, N, C, H, W)
    #   -> expand (K, N, C, H, W) -> reshape (N*K, C, H, W)
    textures = (
        textures.permute(0, 3, 1, 2)[None, ...]
        .expand(K, -1, -1, -1, -1)
        .transpose(0, 1)
        .reshape(N * K, C, H_in, W_in)
    )

    # Textures: (N*K, C, H, W), pixel_uvs: (N*K, H, W, 2)
    # Now need to format the pixel uvs and the texture map correctly!
    # From pytorch docs, grid_sample takes `grid` and `input`:
    #   grid specifies the sampling pixel locations normalized by
    #   the input spatial dimensions It should have most
    #   values in the range of [-1, 1]. Values x = -1, y = -1
    #   is the left-top pixel of input, and values x = 1, y = 1 is the
    #   right-bottom pixel of input.

    # map to a range of [-1, 1] and flip the y axis
    pixel_uvs = torch.lerp(
        pixel_uvs.new_tensor([-1.0, 1.0]),
        pixel_uvs.new_tensor([1.0, -1.0]),
        pixel_uvs,
    )

    if textures.device != pixel_uvs.device:
        textures = textures.to(pixel_uvs.device)
    texels = nn.functional.grid_sample(
        textures,
        pixel_uvs,
        mode="bilinear",
        align_corners=True,
        padding_mode="border",
    )
    # texels now has shape (NK, C, H_out, W_out)
    texels = texels.reshape(N, K, C, H_out, W_out).permute(0, 3, 4, 1, 2)

    return texels

def rasterize_texture(image, vert_uvs, fragments):
    c = image.shape[-1]
    texels = sample_texture(image.flip(2), 1 - vert_uvs, fragments)
    rasterization = hard_rgb_blend(texels, fragments, BlendParams())[...,:c]
    
    return rasterization