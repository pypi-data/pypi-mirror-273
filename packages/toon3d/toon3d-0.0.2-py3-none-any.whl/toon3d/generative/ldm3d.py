"""LDM3D module

Original code at https://github.com/huggingface/diffusers/blob/main/src/diffusers/pipelines/stable_diffusion_ldm3d/pipeline_stable_diffusion_ldm3d.py#L62
More documentation at https://huggingface.co/docs/diffusers/v0.18.2/en/api/pipelines/stable_diffusion/ldm3d_diffusion#diffusers.StableDiffusionLDM3DPipeline
Even more at https://github.com/huggingface/diffusers/blob/7f58a76f485498518edb107666edd1b5a314f324/src/diffusers/image_processor.py#L646
"""

import sys
from pathlib import Path
from typing import List, Optional, Union

import mediapy
import numpy as np
import torch
import torch.nn.functional as F
import tyro
from jaxtyping import Float
from torch import Tensor, nn
from torchvision.transforms.functional import center_crop

from nerfstudio.utils.rich_utils import CONSOLE
from nerfstudio.utils.colormaps import apply_depth_colormap

IMG_DIM = 512
CONST_SCALE = 0.18215


def get_rgbd_vis(rgbd):
    rgb, d = rgbd[:, :3], rgbd[:, 3:4]
    rgb = rgb.permute(0, 2, 3, 1)
    d = d.permute(0, 2, 3, 1)
    shape = d.shape
    d = apply_depth_colormap(d.view(-1, 1)).view(shape[0], shape[1], shape[2], 3)
    rgbd_vis = torch.cat([rgb, d], dim=2)
    return rgbd_vis


def one_to_three_channel_disparity(d: Float[Tensor, "BS 1 H W"]) -> Float[Tensor, "BS 3 H W"]:
    """
    Convert 1-channel disparity to 3-channel disparity in a differentiable manner.

    Args:
        d: 1-channel disparity, normalized to [0, 1]

    Returns:
        3-channel disparity, each channel is simulated 8-bit disparity, normalized to [0, 1]
    """
    # Scale up as if converting to 16-bit disparity
    out = d * 2**16

    # Extract high and low parts
    high_part = torch.floor(out / 256) / 255.0  # High byte, normalized
    low_part = (out / 255.0) % 1.0  # Low byte, normalized

    # Concat and normalize to [0, 1]
    out = torch.cat([torch.zeros_like(high_part), high_part, low_part], dim=1)
    return out


def three_to_one_channel_disparity(d: Float[Tensor, "BS 3 H W"]) -> Float[Tensor, "BS 1 H W"]:
    """Convert 3-channel disparity to 1-channel disparity.

    Args:
        d: 3-channel disparity, each channel is 8-bit disparity, normalized to [0, 1]
    Returns:
        1-channel disparity, 16-bit disparity, normalized to [0, 1]
    """
    out = d * 255.0
    out = out[:, 1:2] * 2**8 + out[:, 2:3]
    out = out / (2**16 - 1)
    return out


class LDM3D(nn.Module):
    """LDM3D implementation
    Args:
        device: device to use
        num_train_timesteps: number of training timesteps
    """

    module_name: str = "LDM3D"

    def __init__(
        self,
        device: Union[torch.device, str] = "cpu",
        num_train_timesteps: int = 1000,
        torch_dtype: torch.dtype = torch.float16,
        lora_weights_path: Optional[Path] = None,
        min_perc: float = 0.02,
        max_perc: float = 0.98,
    ) -> None:
        super().__init__()

        try:
            from diffusers import DiffusionPipeline, StableDiffusionLDM3DPipeline, DDIMScheduler

        except ImportError:
            CONSOLE.print("[bold red]Missing Stable Diffusion packages!")
            sys.exit(1)

        self.device = device
        self.num_train_timesteps = num_train_timesteps
        self.torch_dtype = torch_dtype
        self.lora_weights_path = lora_weights_path
        self.min_perc = min_perc
        self.max_perc = max_perc

        self.min_step = int(self.num_train_timesteps * self.min_perc)
        self.max_step = int(self.num_train_timesteps * self.max_perc)

        CONSOLE.print(f"[bold green]Loading {self.module_name}...")

        pipe = StableDiffusionLDM3DPipeline.from_pretrained(
            "Intel/ldm3d",
            torch_dtype=self.torch_dtype,  # (optional) Run with half-precision (16-bit float).
        )
        assert isinstance(pipe, DiffusionPipeline)  # and hasattr(pipe, "to")
        pipe = pipe.to(self.device)

        # Possibly load lora weights
        if self.lora_weights_path:
            pipe.load_lora_weights(
                str(self.lora_weights_path),
            )

        pipe.enable_attention_slicing()

        self.pipe = pipe

        self.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
        self.alphas = self.scheduler.alphas_cumprod.to(self.device)  # type: ignore

        self.unet = pipe.unet
        self.unet.to(memory_format=torch.channels_last)

        self.tokenizer = pipe.tokenizer
        self.text_encoder = pipe.text_encoder
        self.auto_encoder = pipe.vae

        CONSOLE.print(f"[bold green]{self.module_name} loaded! :tada:")

        self.empty_text_embed = None

    def get_text_embeds(
        self, prompt: Union[str, List[str]], negative_prompt: Union[str, List[str]]
    ) -> Float[Tensor, "2 max_length embed_dim"]:
        """Get text embeddings for prompt and negative prompt
        Args:
            prompt: Prompt text
            negative_prompt: Negative prompt text
        Returns:
            Text embeddings
        """

        # Tokenize text and get embeddings
        text_input = self.tokenizer(
            prompt,
            padding="max_length",
            max_length=self.tokenizer.model_max_length,
            truncation=True,
            return_tensors="pt",
        )

        with torch.no_grad():
            text_embeddings = self.text_encoder(text_input.input_ids.to(self.text_encoder.device))[0]

        # Do the same for unconditional embeddings
        uncond_input = self.tokenizer(
            negative_prompt, padding="max_length", max_length=self.tokenizer.model_max_length, return_tensors="pt"
        )

        with torch.no_grad():
            uncond_embeddings = self.text_encoder(uncond_input.input_ids.to(self.text_encoder.device))[0]

        # Cat for final embeddings
        text_embeddings = torch.cat([uncond_embeddings, text_embeddings])

        return text_embeddings

    def produce_latents(
        self,
        text_embeddings: Float[Tensor, "N max_length embed_dim"],
        height: int = IMG_DIM,
        width: int = IMG_DIM,
        num_inference_steps: int = 50,
        guidance_scale: float = 5.0,
        latents: Optional[Float[Tensor, "BS 4 H W"]] = None,
    ) -> Float[Tensor, "BS 4 H W"]:
        """Produce latents for a given text embedding
        Args:
            text_embeddings: Text embeddings
            height: Height of the image
            width: Width of the image
            num_inference_steps: Number of inference steps
            guidance_scale: How much to weigh the guidance
            latents: Latents to start with
        Returns:
            Latents
        """

        if latents is None:
            latents = torch.randn(
                (text_embeddings.shape[0] // 2, self.unet.config.in_channels, height // 8, width // 8),
                device=self.device,
                dtype=self.torch_dtype,
            )

        self.scheduler.set_timesteps(num_inference_steps)  # type: ignore

        with torch.autocast("cuda"):
            for t in self.scheduler.timesteps:  # type: ignore
                assert latents is not None
                # expand the latents if we are doing classifier-free guidance to avoid doing two forward passes.
                latent_model_input = torch.cat([latents] * 2)
                latent_model_input = self.scheduler.scale_model_input(latent_model_input, t)

                # assert no nans
                assert not torch.isnan(latent_model_input).any(), f"NaNs in latent_model_input at timestep {t}"

                # predict the noise residual
                with torch.no_grad():
                    noise_pred = self.unet(
                        latent_model_input, t.to(self.device), encoder_hidden_states=text_embeddings
                    ).sample

                # assert no nans
                assert not torch.isnan(noise_pred).any(), f"NaNs in noise_pred at timestep {t}"

                # perform guidance
                noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)

                # assert no nans
                assert not torch.isnan(noise_pred_uncond).any(), f"NaNs in noise_pred_uncond at timestep {t}"
                assert not torch.isnan(noise_pred_text).any(), f"NaNs in noise_pred_text at timestep {t}"

                noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)

                # assert no nans
                assert not torch.isnan(noise_pred).any(), f"NaNs in noise_pred at timestep {t}"

                # compute the previous noisy sample x_t -> x_t-1
                latents = self.scheduler.step(noise_pred, t, latents)["prev_sample"]  # type: ignore

                # assert no nans
                # assert not torch.isnan(latents).any(), f"NaNs in latents at timestep {t}"
        assert isinstance(latents, Tensor)
        return latents

    def latents_to_rgbd(
        self, latents: Float[Tensor, "BS 4 H W"], replace_disparity_infs: bool = True
    ) -> Float[Tensor, "BS 4 H W"]:
        """Convert latents to images
        Args:
            latents: Latents to convert
            replace_disparity_infs: Whether to replace inf values in disparity
        Returns:
            RGB and disparity as 4 channels
        """

        latents = 1 / CONST_SCALE * latents

        with torch.no_grad():
            imgs = self.auto_encoder.decode(latents).sample

        imgs = (imgs / 2 + 0.5).clamp(0, 1)

        rgb = imgs[:, :3]
        disparity = three_to_one_channel_disparity(imgs[:, 3:])

        if replace_disparity_infs and torch.isinf(disparity).any():
            # Find the maximum finite value in the tensor
            max_finite_value = disparity[torch.isfinite(disparity)].max()
            # Replace inf values with the maximum finite value
            disparity[torch.isinf(disparity)] = max_finite_value

        rgbd = torch.cat([rgb, disparity], dim=1)

        return rgbd

    def rgbd_to_latents(self, rgbd: Float[Tensor, "BS 4 H W"]) -> Float[Tensor, "BS 4 H W"]:
        """Convert rgbd to latents
        Args:
            rgbd: RGBD to convert
        Returns:
            Latents
        """

        rgb = rgbd[:, :3]
        d = rgbd[:, 3:4]

        # preprocess disparity
        # described in Sec. 3.1.2. https://arxiv.org/pdf/2305.10853.pdf
        ddd = one_to_three_channel_disparity(d)

        # ddd = torch.zeros_like(ddd).to(rgbd)
        rgbddd = torch.cat([rgb, ddd], dim=1) * 2 - 1

        posterior = self.auto_encoder.encode(rgbddd).latent_dist
        latents = posterior.sample() * CONST_SCALE
        return latents

    def prompt_to_rgbd(
        self,
        prompts: Union[str, List[str]],
        negative_prompts: Union[str, List[str]] = "",
        num_inference_steps: int = 50,
        guidance_scale: float = 5.0,
        latents=None,
    ) -> np.ndarray:
        """Generate rgbd images from prompt(s).
        Args:
            prompts: The prompt to generate an image from.
            negative_prompts: The negative prompt to generate an image from.
            num_inference_steps: The number of inference steps to perform.
            guidance_scale: The scale of the guidance.
            latents: The latents to start from, defaults to random.
        Returns:
            The generated image.
        """

        prompts = [prompts] if isinstance(prompts, str) else prompts
        negative_prompts = [negative_prompts] if isinstance(negative_prompts, str) else negative_prompts
        prompt_embeds = self.get_text_embeds(prompts, negative_prompts)
        latents = self.produce_latents(
            text_embeddings=prompt_embeds,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            latents=latents,
        )
        rgbd = self.latents_to_rgbd(latents.to(self.torch_dtype))
        return rgbd

    def sds_loss(
        self,
        text_embeddings: Float[Tensor, "N max_length embed_dim"],
        rgbd: Float[Tensor, "BS 4 H W"],
        guidance_scale: float = 10.0,
    ) -> torch.Tensor:
        """Score Distilation Sampling loss proposed in DreamFusion paper (https://dreamfusion3d.github.io/)
        Args:
            text_embeddings: Text embeddings
            rgbd: Rendered rgbd image
            guidance_scale: How much to weigh the guidance
        Returns:
            The loss
        """
        # Enable autocast for mixed precision
        # TODO: can we eliminate autocast?
        with torch.autocast("cuda"):
            rgbd = F.interpolate(rgbd, (IMG_DIM, IMG_DIM), mode="bilinear")
            t = torch.randint(self.min_step, self.max_step + 1, [1], dtype=torch.long, device=self.device)
            latents = self.rgbd_to_latents(rgbd)

            # predict the noise residual with unet, NO grad!
            with torch.no_grad():
                # add noise
                noise = torch.randn_like(latents)
                latents_noisy = self.scheduler.add_noise(latents, noise, t)  # type: ignore
                # pred noise
                latent_model_input = torch.cat((latents_noisy,) * 2)
                noise_pred = self.unet(latent_model_input, t, encoder_hidden_states=text_embeddings).sample

            # perform guidance
            noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
            noise_pred = noise_pred_text + guidance_scale * (noise_pred_text - noise_pred_uncond)

            # w(t), sigma_t^2
            w = 1 - self.alphas[t]

            grad = w * (noise_pred - noise)
            grad = torch.nan_to_num(grad)

            target = (latents - grad).detach()
            loss = 0.5 * F.mse_loss(latents, target, reduction="sum") / latents.shape[0]

            return loss


if __name__ == "__main__":
    ldm3d = LDM3D(device="cuda:0")
    prompt = "a photo of a cartoon house"
    negative_prompt = ""
    rgbd = ldm3d.prompt_to_rgbd(prompt, negative_prompt)
    rgbd_vis = get_rgbd_vis(rgbd)
    mediapy.write_image("test_ldm3d.png", rgbd_vis[0].detach().cpu())
