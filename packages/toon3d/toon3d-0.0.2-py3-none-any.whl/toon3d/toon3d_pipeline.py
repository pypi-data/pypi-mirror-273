# Copyright 2022 The Nerfstudio Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Toon3D pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Type
import torch
from torch.cuda.amp.grad_scaler import GradScaler
from typing_extensions import Literal
from nerfstudio.pipelines.base_pipeline import VanillaPipeline, VanillaPipelineConfig
from toon3d.toon3d_model import Toon3DModelConfig
from toon3d.utils.tsdf_utils import export_tsdf_mesh
from pathlib import Path


@dataclass
class Toon3DPipelineConfig(VanillaPipelineConfig):
    """Configuration for pipeline instantiation"""

    _target: Type = field(default_factory=lambda: Toon3DPipeline)
    """target class to instantiate"""


class Toon3DPipeline(VanillaPipeline):
    """InstructNeRF2NeRF pipeline"""

    config: Toon3DPipelineConfig

    def __init__(
        self,
        config: Toon3DPipelineConfig,
        device: str,
        test_mode: Literal["test", "val", "inference"] = "val",
        world_size: int = 1,
        local_rank: int = 0,
        grad_scaler: Optional[GradScaler] = None,
    ):
        super(VanillaPipeline, self).__init__()

        # modify the config for nd attributes
        if config.model.use_color_palette:
            print("Overriding nd_dim config based on color palette config")
            config.model.use_nd = True
            config.model.nd_dim = config.datamanager.num_colors

        self.config = config
        self.test_mode = test_mode
        self.datamanager: DataManager = config.datamanager.setup(
            device=device, test_mode=test_mode, world_size=world_size, local_rank=local_rank
        )
        # TODO make cleaner
        seed_pts = None
        if (
            hasattr(self.datamanager, "train_dataparser_outputs")
            and "points3D_xyz" in self.datamanager.train_dataparser_outputs.metadata
        ):
            pts = self.datamanager.train_dataparser_outputs.metadata["points3D_xyz"]
            pts_rgb = self.datamanager.train_dataparser_outputs.metadata["points3D_rgb"]
            seed_pts = (pts, pts_rgb)
        self.datamanager.to(device)
        # TODO(ethan): get rid of scene_bounds from the model
        assert self.datamanager.train_dataset is not None, "Missing input dataset"

        assert isinstance(config.model, Toon3DModelConfig), "Model config must be Toon3DModelConfg"

        color_palette = self.datamanager.color_palette
        images = [self.datamanager.cached_train[i]["image"] for i in range(len(self.datamanager.cached_train))]
        points = self.datamanager.train_dataparser_outputs.metadata["points"]
        points_mask = self.datamanager.train_dataparser_outputs.metadata["points_mask"]
        mesh_points = self.datamanager.train_dataparser_outputs.metadata["mesh_points"]
        warped_mesh_points = self.datamanager.train_dataparser_outputs.metadata["warped_mesh_points"]
        simplices = self.datamanager.train_dataparser_outputs.metadata["simplices"]
        cameras = self.datamanager.train_dataparser_outputs.cameras
        points3D_xyz = self.datamanager.train_dataparser_outputs.metadata["points3D_xyz"]

        # compute the TSDF
        # depth_images = [self.datamanager.cached_train[i]["depth_image"] for i in range(len(self.datamanager.cached_train))]
        # color_images = [self.datamanager.cached_train[i]["image"] for i in range(len(self.datamanager.cached_train))]
        # res = 512
        # scale = 2.0
        # bounding_box_min = (-scale, -scale, -scale)
        # bounding_box_max = (scale, scale, scale)
        # tsdf = export_tsdf_mesh(
        #     cameras=cameras,
        #     depth_images=depth_images,
        #     color_images=color_images,
        #     output_dir=Path('.'),
        #     device=device,
        #     resolution=[res, res, res],
        #     bounding_box_min=bounding_box_min,
        #     bounding_box_max=bounding_box_max)

        # import pdb; pdb.set_trace();
        self._model = config.model.setup(
            scene_box=self.datamanager.train_dataset.scene_box,
            num_train_data=len(self.datamanager.train_dataset),
            metadata=self.datamanager.train_dataset.metadata,
            device=device,
            grad_scaler=grad_scaler,
            seed_points=seed_pts,
            color_palette=color_palette,
            images=images,
            points=points,
            points_mask=points_mask,
            mesh_points=mesh_points,
            warped_mesh_points=warped_mesh_points,
            simplices=simplices,
            cameras=cameras,
            points3D_xyz=points3D_xyz,
        )
        self.model.to(device)
        if self.model.config.use_sds:
            # TODO(ethan): this is hacky and should be fixed
            self.model.diffusion_model.to(self.model.config.sds_device)

        self.world_size = world_size
        if world_size > 1:
            self._model = typing.cast(Model, DDP(self._model, device_ids=[local_rank], find_unused_parameters=True))
            dist.barrier(device_ids=[local_rank])
