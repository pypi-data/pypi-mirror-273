"""
Code for color palettes.
"""

import torch
from kmeans_pytorch import kmeans


def color_cluster_kmeans(
    images: torch.tensor,
    num_colors: int,
    color_palette_downscale: int = 1,
    nearest_neighbor: bool = False,
    num_pixel_samples_for_nn: int = 1000,
):
    """Returns palettized images and the color palette.

    Args:
        images: tensor of shape (N, H, W, 3)
        num_colors: number of colors to put in palette
        color_palette_downscale: downscale factor for images before clustering
        nearest_neighbor: whether to use nearest neighbor to find the closest color in the image to each cluster center
        num_pixel_samples_for_nn: number of pixels to sample from the image to find the closest color in the image to each cluster center
    """
    device = images.device
    image_flattened = images.reshape(-1, 3)[::color_palette_downscale]
    _, cluster_centers = kmeans(
        X=image_flattened,
        num_clusters=num_colors,
        device=device,
    )
    cluster_centers = cluster_centers.to(device)
    color_palette = cluster_centers
    if nearest_neighbor:
        # find closest color in images to each cluster center
        random_pixels_from_flattened_images = image_flattened[
            torch.randint(0, image_flattened.shape[0], (num_pixel_samples_for_nn,))
        ]
        image_color_centers = random_pixels_from_flattened_images[
            torch.argmin(torch.cdist(cluster_centers, random_pixels_from_flattened_images), dim=-1)
        ]
        color_palette = image_color_centers

    dist = torch.cdist(images, color_palette)
    ind = torch.argmin(dist, dim=-1)
    paletizzed_images = color_palette[ind]
    return paletizzed_images, color_palette
