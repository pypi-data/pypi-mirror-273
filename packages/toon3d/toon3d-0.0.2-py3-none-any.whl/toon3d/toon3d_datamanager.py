"""
Template DataManager
"""

from dataclasses import dataclass, field
from typing import Dict, Literal, Tuple, Type

import torch

from nerfstudio.data.datamanagers.full_images_datamanager import FullImageDatamanagerConfig, FullImageDatamanager
import matplotlib.pyplot as plt
import mediapy
from toon3d.color_palette import color_cluster_kmeans
from kornia.color import rgb_to_lab, lab_to_rgb, rgb_to_hsv, hsv_to_rgb
from nerfstudio.data.datasets.depth_dataset import DepthDataset


@dataclass
class Toon3DDataManagerConfig(FullImageDatamanagerConfig):
    """Toon3D DataManager Config

    Add your custom datamanager config parameters here.
    """

    # color palette parameters
    use_color_palette: bool = False
    palette_type: str = "hsv_kmeans"
    color_palette_downscale: float = 1
    num_colors: int = 8

    _target: Type = field(default_factory=lambda: Toon3DDataManager)


class Toon3DDataManager(FullImageDatamanager[DepthDataset]):
    """Toon3D DataManager

    Args:
        config: the Toon3DDataManager used to instantiate class
    """

    config: Toon3DDataManagerConfig

    def __init__(self, config: Toon3DDataManagerConfig, **kwargs):
        self.color_palette = None
        super().__init__(config)

    def setup_train(self):
        """Setup the train dataloader."""
        self.device = "cuda:0"

        # TODO: assert that we are using the same images for both train and eval

        # compute the color palette
        if self.config.use_color_palette:
            images = torch.stack([self.cached_train[i]["image"] for i in range(len(self.cached_train))]).to(self.device)

            if self.config.palette_type == "rgb_kmeans":
                paletizzed_images, cluster_centers = color_cluster_kmeans(
                    images, self.config.num_colors, self.config.color_palette_downscale
                )
            elif self.config.palette_type == "rgb_kmeans_nn":
                paletizzed_images, cluster_centers = color_cluster_kmeans(
                    images, self.config.num_colors, self.config.color_palette_downscale, nearest_neighbor=True
                )
            elif self.config.palette_type == "hsv_kmeans":
                images_hsv = rgb_to_hsv(images.permute(0, 3, 1, 2)).permute(0, 2, 3, 1)
                paletizzed_images, cluster_centers = color_cluster_kmeans(
                    images_hsv, self.config.num_colors, self.config.color_palette_downscale
                )
                cluster_centers = hsv_to_rgb(cluster_centers[..., None, None])[..., 0, 0]
                paletizzed_images = hsv_to_rgb(paletizzed_images.permute(0, 3, 1, 2)).permute(0, 2, 3, 1)
            elif self.config.palette_type == "hsv_kmeans_nn":
                images_hsv = rgb_to_hsv(images.permute(0, 3, 1, 2)).permute(0, 2, 3, 1)
                paletizzed_images, cluster_centers = color_cluster_kmeans(
                    images_hsv, self.config.num_colors, self.config.color_palette_downscale, nearest_neighbor=True
                )
                cluster_centers = hsv_to_rgb(cluster_centers[..., None, None])[..., 0, 0]
                paletizzed_images = hsv_to_rgb(paletizzed_images.permute(0, 3, 1, 2)).permute(0, 2, 3, 1)
            elif self.config.palette_type == "lab_kmeans":
                images_lab = rgb_to_lab(images.permute(0, 3, 1, 2)).permute(0, 2, 3, 1)
                paletizzed_images, cluster_centers = color_cluster_kmeans(
                    images_lab, self.config.num_colors, self.config.color_palette_downscale
                )
                cluster_centers = lab_to_rgb(cluster_centers[..., None, None])[..., 0, 0]
                paletizzed_images = lab_to_rgb(paletizzed_images.permute(0, 3, 1, 2)).permute(0, 2, 3, 1)
            elif self.config.palette_type == "lab_kmeans_nn":
                images_lab = rgb_to_lab(images.permute(0, 3, 1, 2)).permute(0, 2, 3, 1)
                paletizzed_images, cluster_centers = color_cluster_kmeans(
                    images_lab, self.config.num_colors, self.config.color_palette_downscale, nearest_neighbor=True
                )
                cluster_centers = lab_to_rgb(cluster_centers[..., None, None])[..., 0, 0]
                paletizzed_images = lab_to_rgb(paletizzed_images.permute(0, 3, 1, 2)).permute(0, 2, 3, 1)
            else:
                raise ValueError(f"Invalid palette type {self.config.palette_type}")

            self.color_palette = cluster_centers

            # save to cached images
            for i in range(len(self.cached_train)):
                self.cached_train[i]["image"] = paletizzed_images[i]
                self.cached_train[i]["color_palette"] = self.color_palette
            for i in range(len(self.cached_eval)):
                self.cached_eval[i]["image"] = paletizzed_images[i]
                self.cached_eval[i]["color_palette"] = self.color_palette

            # TODO: save visualization files elsewhere

            # visualize the color palette
            fig, ax = plt.subplots()
            for i, (r, g, b) in enumerate(cluster_centers):
                r, g, b = int(r * 255), int(g * 255), int(b * 255)
                color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
                ax.bar(i, 1, color=color_hex, label=color_hex)
            ax.set_xticks(range(len(cluster_centers)))
            ax.set_xticklabels(["Color {}".format(i + 1) for i in range(len(cluster_centers))])
            ax.set_title("RGB Colors")
            plt.savefig(f"color_palette-{self.config.palette_type}-graph.png")

            # show image with the color palette
            mediapy.write_image(
                f"color_palette-{self.config.palette_type}-images.png",
                torch.cat(
                    [
                        torch.cat(list(images.detach().cpu()), dim=1),
                        torch.cat(list(paletizzed_images.detach().cpu()), dim=1),
                    ],
                ),
            )
