"""
TSDF utils.
"""


from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple, Union

import numpy as np
import pymeshlab
import torch
import torch.nn.functional as F
from jaxtyping import Bool, Float
from skimage import measure
from torch import Tensor

from nerfstudio.exporter.exporter_utils import Mesh, render_trajectory
from nerfstudio.pipelines.base_pipeline import Pipeline
from nerfstudio.utils.rich_utils import CONSOLE

from nerfstudio.exporter.tsdf_utils import TSDF
from nerfstudio.cameras.cameras import Cameras

TORCH_DEVICE = Union[torch.device, str]

def export_tsdf_mesh(
    cameras: Cameras,
    depth_images: List[Float[Tensor, "H W 1"]],
    color_images: List[Float[Tensor, "H W 3"]],
    output_dir: Path,
    device: TORCH_DEVICE,
    resolution: Union[int, List[int]] = field(default_factory=lambda: [256, 256, 256]),
    bounding_box_min: Tuple[float, float, float] = (-1.0, -1.0, -1.0),
    bounding_box_max: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> None:
    """Export a TSDF mesh from a pipeline.

    Args:
        output_dir: The directory to save the mesh to.
        resolution: Resolution of the TSDF volume or [x, y, z] resolutions individually.
        bounding_box_min: Minimum coordinates of the bounding box.
        bounding_box_max: Maximum coordinates of the bounding box.
    """

    aabb = torch.tensor([bounding_box_min, bounding_box_max])
    if isinstance(resolution, int):
        volume_dims = torch.tensor([resolution] * 3)
    elif isinstance(resolution, List):
        volume_dims = torch.tensor(resolution)
    else:
        raise ValueError("Resolution must be an int or a list.")
    tsdf = TSDF.from_aabb(aabb, volume_dims=volume_dims)
    # move TSDF to device
    tsdf.to(device)

    # camera extrinsics and intrinsics
    c2w: Float[Tensor, "N 3 4"] = cameras.camera_to_worlds.to(device)
    # make c2w homogeneous
    c2w = torch.cat([c2w, torch.zeros(c2w.shape[0], 1, 4, device=device)], dim=1)
    c2w[:, 3, 3] = 1
    K: Float[Tensor, "N 3 3"] = cameras.get_intrinsics_matrices().to(device)

    CONSOLE.print("Integrating the TSDF")
    for i in range(0, len(c2w)):
        di = depth_images[i][None].permute(0, 3, 1, 2).to(device)
        ci = color_images[i][None].permute(0, 3, 1, 2).to(device)
        tsdf.integrate_tsdf(
            c2w[i : i + 1],
            K[i : i + 1],
            di,
            ci
        )

    CONSOLE.print("Computing Mesh")
    mesh = tsdf.get_mesh()
    CONSOLE.print("Saving TSDF Mesh")
    tsdf.export_mesh(mesh, filename=str(output_dir / "tsdf_mesh.ply"))
    return tsdf
