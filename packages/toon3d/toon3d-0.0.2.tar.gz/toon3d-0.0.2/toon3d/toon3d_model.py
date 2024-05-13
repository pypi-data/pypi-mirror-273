"""
Toon3D model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Type
import torch
from torch.nn import Parameter
from nerfstudio.models.splatfacto import SplatfactoModel, SplatfactoModelConfig, projection_matrix

import torch
from torch.nn import Parameter

from toon3d.warp.warp_mesh import WarpMesh
from toon3d.utils.losses import depth_ranking_loss

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Type, Union

import numpy as np
import torch
import torchvision.transforms.functional as TF
from gsplat._torch_impl import quat_to_rotmat

from gsplat.project_gaussians import project_gaussians
from gsplat.rasterize import rasterize_gaussians
from gsplat.sh import num_sh_bases, spherical_harmonics
from pytorch_msssim import SSIM
from sklearn.neighbors import NearestNeighbors
from torch.nn import Parameter
from torchmetrics.image import PeakSignalNoiseRatio
from torchmetrics.image.lpip import LearnedPerceptualImagePatchSimilarity

from nerfstudio.cameras.cameras import Cameras
from nerfstudio.data.scene_box import OrientedBox
from nerfstudio.engine.callbacks import TrainingCallback, TrainingCallbackAttributes, TrainingCallbackLocation
from nerfstudio.engine.optimizers import Optimizers

# need following import for background color override
from nerfstudio.model_components import renderers
from nerfstudio.model_components.losses import tv_loss
from nerfstudio.models.base_model import Model, ModelConfig
from nerfstudio.utils.rich_utils import CONSOLE
from nerfstudio.utils.colormaps import apply_depth_colormap

from toon3d.generative.ldm3d import LDM3D
import mediapy
from toon3d.configs.prompts import get_prompts
from toon3d.utils.novel_view_samplers import sample_interpolated_camera
from toon3d.utils.depth_utils import depth_to_disparity
from pytorch3d.loss.chamfer import chamfer_distance
from nerfstudio.viewer.viewer_elements import ViewerControl
from nerfstudio.viewer.viewer import VISER_NERFSTUDIO_SCALE_RATIO


@dataclass
class Toon3DModelConfig(SplatfactoModelConfig):
    """Config for the toon3d model."""

    _target: Type = field(default_factory=lambda: Toon3DModel)

    # warp parameters
    warp_images: bool = False
    """Warp input images"""

    # color palette parameters
    use_color_palette: bool = False
    """Whether to use the color palette for the toon3d model."""
    color_palette_project_before_render: bool = False
    """Whether to project nd dim with the color palette before rendering."""
    color_palette_use_as_colors: bool = False
    """Whether to use the color palette as the rgb output of the model."""
    color_palette_mult: float = 1.0
    """Multiplier for the color palette loss, when using it as a regularizer (not rgb)."""
    color_palette_rend_consistency_mult: float = 1.0
    """Multiplier for the color palette rendered consistency loss, when using it as a regularizer (not rgb)."""

    # depth regularization parameters
    use_tv_loss: bool = True
    """Whether to use the total variation loss."""
    tv_loss_mult: float = 100.0
    """Multiplier for the total variation loss."""
    tv_loss_strides: List[int] = field(default_factory=lambda: [1])
    """Downscale strides to use for the total variation loss."""
    use_tv_in_novel_views: bool = True
    """Whether to use the total variation loss in novel views."""
    tv_in_novel_views_loss_mult: float = 100.0
    """Multiplier for the total variation loss in novel views."""
    tv_in_novel_views_loss_strides: List[int] = field(default_factory=lambda: [1])
    """Downscale strides to use for the total variation loss in novel views."""
    use_depth_ranking_loss: bool = True
    """Whether to use the depth ranking loss."""
    depth_ranking_loss_mult: float = 1.0
    """Multiplier for the depth ranking loss."""
    depth_ranking_loss_patch_size: int = 128
    """Patch size for the depth ranking loss."""
    depth_ranking_loss_num_patches: int = 8
    """Number of patches to sample for the depth ranking loss."""
    use_depth_loss: bool = False
    """Whether to use the depth loss."""
    depth_loss_mult: float = 1.0
    """Multiplier for the depth loss."""

    # sds parameters
    use_sds: bool = False
    """Whether to use the sds loss."""
    sds_mult: float = 1.0
    """Multiplier for the sds loss."""
    steps_per_sds: int = 10
    """Number of steps per sds loss."""
    sds_device: str = "cuda:1"
    """device for sds diffusion model"""
    sds_guidance_scale: float = 10.0
    """Guidance scale for sds loss."""
    sds_dataset: Optional[str] = None
    """Dataset for sds model."""
    sds_lora_weights_path: Optional[str] = None
    """Path to the lora weights for sds model."""

    use_chamfer_loss: bool = False
    """Whether to use the chamfer loss."""
    chamfer_loss_mult: float = 1.0
    """Multiplier for the chamfer loss."""
    chamfer_loss_num_points: int = 10000
    """Number of points to use for the chamfer loss."""

    use_isotropic_loss: bool = False
    """Whether to use the isotropic loss."""
    isotropic_ratio_mult: float = 1e6
    """Multiplier for the isotropic ratio loss."""

    use_ratio_loss: bool = True
    """Whether to use the ratio loss."""
    ratio_loss_mult: float = 1e6
    """Multiplier for the ratio loss."""
    max_ratio_ratio: float = 10.0
    """threshold of ratio of gaussian max to min scale before applying regularization
    loss from the PhysGaussian paper
    """

class Toon3DModel(SplatfactoModel):
    """Model for toon3d."""

    config: Toon3DModelConfig

    def __init__(self, *args, **kwargs):
        self.color_palette = kwargs["color_palette"]
        self.images = kwargs["images"]
        self.points = kwargs["points"]
        self.points_mask = kwargs["points_mask"]
        self.mesh_points = kwargs["mesh_points"]
        self.warped_mesh_points = kwargs["warped_mesh_points"]
        self.simplices_list = kwargs["simplices"]
        self.cameras = kwargs["cameras"]
        self.points3D_xyz = kwargs["points3D_xyz"]
        self.devic = kwargs["device"] # would be device but otherwise get a AttributeError: can't set attribute
        super().__init__(*args, **kwargs)

    def populate_modules(self):
        """Required for our custom models."""

        # modify the config for nd attributes
        if self.config.use_color_palette:
            print("Overriding nd_dim config based on color palette config")
            if self.config.color_palette_use_as_colors:
                self.config.nd_detach = False
            else:
                self.config.nd_detach = True

        super().populate_modules()

        # import pdb; pdb.set_trace();
        self.iters = 0

        # warping modules
        if self.config.warp_images:
            corr_points_list = self.mesh_points["corr_points"]
            boundary_points_list = self.mesh_points["boundary_points"]
            inner_points_list = self.mesh_points["inner_points"]

            warped_corr_points_list = self.warped_mesh_points["corr_points"]
            warped_boundary_points_list = self.warped_mesh_points["boundary_points"]
            warped_inner_points_list = self.warped_mesh_points["inner_points"]

            original_mesh_points_list = [torch.cat(wmp_triple) for wmp_triple in zip(corr_points_list, boundary_points_list, inner_points_list)]
            warped_mesh_points_list = [torch.cat(wmp_triple) for wmp_triple in zip(warped_corr_points_list, warped_boundary_points_list, warped_inner_points_list)]

            self.meshes = []

            for ndx in range(len(self.images)):
                image = self.images[ndx]
                height, width = image.shape[:2]

                uv_points = original_mesh_points_list[ndx]
                warped_mesh_points = warped_mesh_points_list[ndx]
                simplices = self.simplices_list[ndx]

                mesh = WarpMesh(warped_mesh_points, simplices, height, width, uv_points, device=self.devic)

                self.meshes.append(mesh)

        # we toggle this on and off
        # when True, we perturb the camera and apply an SDS loss
        self.perturb_camera = False
        if self.config.use_sds:
            if not self.config.sds_dataset:
                raise ValueError("--pipeline.model.sds_dataset must be provided when using SDS")
            self.diffusion_model = LDM3D(
                device=self.config.sds_device, lora_weights_path=self.config.sds_lora_weights_path
            )
            prompts, negative_prompts = get_prompts(self.config.sds_dataset)
            self.text_embeddings = self.diffusion_model.get_text_embeds(prompts, negative_prompts)

    def get_training_callbacks(
        self, training_callback_attributes: TrainingCallbackAttributes
    ) -> List[TrainingCallback]:
        cbs = super().get_training_callbacks(training_callback_attributes)

        if self.config.use_sds or self.config.use_tv_in_novel_views:

            def toggle_perturb(step, **kwargs):
                if step != 0 and step % self.config.steps_per_sds == 0:
                    self.perturb_camera = not self.perturb_camera

            cbs.append(
                TrainingCallback(
                    [TrainingCallbackLocation.BEFORE_TRAIN_ITERATION, TrainingCallbackLocation.AFTER_TRAIN_ITERATION],
                    toggle_perturb,
                )
            )
        return cbs

    def get_param_groups(self) -> Dict[str, List[Parameter]]:
        """Obtain the parameter groups for the optimizers

        Returns:
            Mapping of different parameter groups
        """
        gps = super().get_param_groups()

        # custom params
        # TODO:
        return gps

    def get_outputs(self, camera: Cameras) -> Dict[str, Union[torch.Tensor, List]]:
        """Takes in a Ray Bundle and returns a dictionary of outputs.

        Args:
            ray_bundle: Input bundle of rays. This raybundle should have all the
            needed information to compute the outputs.

        Returns:
            Outputs of model. (ie. rendered colors)
        """

        if self.perturb_camera:
            camera_perturb = sample_interpolated_camera(self.cameras)
            camera_perturb = camera_perturb.reshape(camera.shape).to(camera.device)
            outputs = super().get_outputs(camera_perturb)
            # mediapy.write_image("novel_view.png", outputs["rgb"].detach().cpu())
        else:
            outputs = super().get_outputs(camera)
        return outputs

    def get_nd_values(self):
        if self.config.use_color_palette and self.config.color_palette_project_before_render:
            sm = torch.softmax(self.nd_values, dim=-1)[..., None]
            cp = self.color_palette[None]
            nd_values = torch.sum(sm * cp, dim=-2)
            return nd_values
        else:
            return self.nd_values

    def get_color_palette_rgb(self, nd_value):
        if self.config.use_color_palette and self.config.color_palette_project_before_render:
            return nd_value
        else:
            sm = torch.softmax(nd_value, dim=-1)[..., None]
            cp = self.color_palette[None, None]
            return torch.sum(sm * cp, dim=-2)

    def get_metrics_dict(self, outputs, batch) -> Dict[str, torch.Tensor]:
        """Compute and returns metrics.

        Args:
            outputs: the output to compute loss dict to
            batch: ground truth batch corresponding to outputs
        """
        gt_rgb = self.get_gt_img(batch["image"])
        metrics_dict = {}

        if self.perturb_camera:
            return metrics_dict

        predicted_rgb = outputs["rgb"]
        metrics_dict["psnr"] = self.psnr(predicted_rgb, gt_rgb)

        metrics_dict["gaussian_count"] = self.num_points
        return metrics_dict

    def get_loss_dict(self, outputs, batch, metrics_dict=None) -> Dict[str, torch.Tensor]:
        """Computes and returns the losses dict.

        Args:
            outputs: the output to compute loss dict to
            batch: ground truth batch corresponding to outputs
            metrics_dict: dictionary of metrics, some of which we can use for loss
        """
        loss_dict = {}
        # import pdb; pdb.set_trace();
        assert "mask" in batch, "mask must be in batch"

        if self.perturb_camera:
            if self.config.use_sds:
                disparity = depth_to_disparity(outputs["depth"][None])[0]
                rgbd = torch.cat([outputs["rgb"], disparity], dim=-1).permute(2, 0, 1)[None]
                rgbd = rgbd.to(self.config.sds_device)
                sds_loss = self.diffusion_model.sds_loss(
                    self.text_embeddings,
                    rgbd,
                    guidance_scale=self.config.sds_guidance_scale,
                )
                loss_dict["sds"] = sds_loss.to(self.device)
            if self.config.use_tv_in_novel_views:
                pred_depth = outputs["depth"]
                for stride in self.config.tv_in_novel_views_loss_strides:
                    l = self.config.tv_in_novel_views_loss_mult * tv_loss(pred_depth.permute(2, 0, 1)[None, :, ::stride, ::stride])
                    if l > 0:
                        loss_dict[f"depth_tv_in_novel_views_loss_stride-{stride}"] = l
            # hack to avoid having no gradients for backprop
            loss_dict["hack"] = (self.xys * 0).sum()
            return loss_dict

        # dense warp for image
        image_idx = batch["image_idx"]
        image = batch["image"] # (height, width, 3)
        mask = batch["mask"].to(image.device)[..., 0] # (height, width)
        depth = batch["depth_image"] # (height, width, 1)

        # import pdb; pdb.set_trace()

        if self.config.warp_images:
            mesh = self.meshes[image_idx]
            fragments = mesh.rasterize()
            image = mesh.render(image, fragments)
            mask = mesh.render(mask.float(), fragments)[...,0] > 0.5
            depth = mesh.render(depth, fragments)

        # mediapy.write_image("image.png", image.detach().cpu())
        # mediapy.write_image("mask.png", (mask.float()).detach().cpu())
        # mediapy.write_image("depth.png", apply_depth_colormap(depth).detach().cpu())

        # import pdb; pdb.set_trace();
        self.iters += 1

        assert self._get_downscale_factor() == 1, "downscale factor must be 1 for toon3d model"

        gt_img = image

        # rgb loss
        if self.config.use_color_palette and self.config.color_palette_use_as_colors:
            rgb = outputs["nd_value"] * mask[...,None].to(outputs["nd_value"].device)
        else:
            rgb = outputs["rgb"] * mask[...,None].to(outputs["rgb"].device)

        Ll1 = torch.abs(gt_img[mask] - rgb[mask]).mean()
        loss_dict["rgb"] = Ll1

        # color palette as a regularizer
        if self.config.use_color_palette and not self.config.color_palette_use_as_colors:
            color_palette_rgb = self.get_color_palette_rgb(outputs["nd_value"])
            # color palette loss
            Ll1 = torch.abs(gt_img[mask] - color_palette_rgb[mask]).mean()
            loss_dict["rgb-cpalette"] = Ll1

            # color consistency loss
            loss_dict["rgb-cpalette-rend-consistency"] = (
                self.config.color_palette_rend_consistency_mult
                * torch.abs(rgb[mask] - color_palette_rgb[mask].detach()).mean()
            )

        if self.config.use_tv_loss:
            pred_depth = outputs["depth"]
            for stride in self.config.tv_loss_strides:
                loss_dict[f"depth_tv_loss_stride-{stride}"] = self.config.tv_loss_mult * tv_loss(
                    pred_depth.permute(2, 0, 1)[None, :, ::stride, ::stride]
                )

        if self.config.use_depth_ranking_loss:
            pred_depth = outputs["depth"]
            gt_depth = depth.to(pred_depth.device)
            mask = mask.to(pred_depth.device)
            loss_dict["depth_ranking_loss"] = (
                self.config.depth_ranking_loss_mult
                * depth_ranking_loss(
                    rendered_depth=pred_depth.permute(2, 0, 1)[None, 0],
                    gt_depth=gt_depth.permute(2, 0, 1)[None, 0],
                    mask=mask[...,None].permute(2, 0, 1)[None, 0],
                    patch_size=self.config.depth_ranking_loss_patch_size,
                    num_patches=self.config.depth_ranking_loss_num_patches,
                ).mean()
            )

        if self.config.use_depth_loss:
            pred_depth = outputs["depth"]
            gt_depth = depth.to(pred_depth.device)
            loss_dict["depth_loss"] = self.config.depth_loss_mult * torch.abs(pred_depth[mask] - gt_depth[mask]).mean()

        if self.config.use_chamfer_loss:
            indices = torch.randperm(self.points3D_xyz.shape[0])[:self.config.chamfer_loss_num_points]
            points3D_xyz = self.points3D_xyz[indices].to(self.means.device)
            chamfer_loss = chamfer_distance(self.means[None], points3D_xyz[None], single_directional=True)[0]
            loss_dict["chamfer_loss"] = self.config.chamfer_loss_mult * chamfer_loss

        if self.config.use_isotropic_loss:
            scale_var = torch.mean(torch.var(self.scales, dim=1))
            loss_dict["isotropic_loss"] = self.config.isotropic_ratio_mult * scale_var

        if self.config.use_ratio_loss:
            scale_exp = torch.exp(self.scales)
            scale_reg = (
                torch.maximum(
                    scale_exp.amax(dim=-1) / scale_exp.amin(dim=-1),
                    torch.tensor(self.config.max_ratio_ratio),
                )
                - self.config.max_ratio_ratio
            )
            scale_reg = self.config.ratio_loss_mult * scale_reg.mean()

        return loss_dict
