# Copyright 2022 the Regents of the University of California, Nerfstudio Team and contributors. All rights reserved.
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
""" Data parser for toon3d datasets. """

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional, Type

import torch

from nerfstudio.data.dataparsers.nerfstudio_dataparser import Nerfstudio, NerfstudioDataParserConfig
from nerfstudio.utils.io import load_from_json


@dataclass
class Toon3DDataParserConfig(NerfstudioDataParserConfig):
    """Toon3D dataset config"""

    _target: Type = field(default_factory=lambda: Toon3D)
    """target class to instantiate"""


@dataclass
class Toon3D(Nerfstudio):
    """Toon3D DatasetParser"""

    config: Toon3DDataParserConfig

    def _generate_dataparser_outputs(self, split="train"):
        dataparser_outputs = super()._generate_dataparser_outputs(split=split)

        if self.config.data.suffix == ".json":
            meta = load_from_json(self.config.data)
            data_dir = self.config.data.parent
        else:
            meta = load_from_json(self.config.data / "transforms.json")
            data_dir = self.config.data

        # import pdb; pdb.set_trace();
        dataparser_outputs.metadata["points"] = torch.load(data_dir / meta["points"])
        dataparser_outputs.metadata["points_mask"] = torch.load(data_dir / meta["points_mask"])
        dataparser_outputs.metadata["mesh_points"] = torch.load(data_dir / meta["meshes_points"])
        dataparser_outputs.metadata["warped_mesh_points"] = torch.load(data_dir / meta["warped_meshes_points"])
        dataparser_outputs.metadata["simplices"] = torch.load(data_dir / meta["simplices"])

        return dataparser_outputs
