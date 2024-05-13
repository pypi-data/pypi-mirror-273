"""
Fine-tune a diffusion model on our data

Relevant reference code at https://github.com/huggingface/diffusers/blob/main/examples/dreambooth/train_dreambooth_lora.py
"""

import argparse
import gc
import itertools
import logging
import math
import multiprocessing
import os
import shutil
from pathlib import Path
from typing import Dict, Union

import glob
import tyro

import numpy as np
import torch
import torch.nn.functional as F
import torch.utils.checkpoint
import transformers
from accelerate import Accelerator
from accelerate.logging import get_logger
from accelerate.utils import ProjectConfiguration, set_seed
from packaging import version
from peft import LoraConfig
from peft.utils import get_peft_model_state_dict, set_peft_model_state_dict
from torchvision import transforms
from tqdm.auto import tqdm

import diffusers
from diffusers import (
    AutoencoderKL,
    DDPMScheduler,
    DPMSolverMultistepScheduler,
    StableDiffusionInpaintPipeline,
    UNet2DConditionModel,
)

# from peft.utils import get_peft_model_state_dict, set_peft_model_state_dict
from diffusers.models.attention_processor import (
    AttnAddedKVProcessor,
    AttnAddedKVProcessor2_0,
    SlicedAttnAddedKVProcessor,
)
from diffusers.models.lora import LoRALinearLayer
from diffusers.optimization import get_scheduler
from diffusers.utils import is_wandb_available, convert_state_dict_to_diffusers
from diffusers.utils.import_utils import is_xformers_available
from diffusers.training_utils import unet_lora_state_dict
from typing import Literal, List, Dict, Optional

from datetime import datetime
from toon3d.configs.prompts import get_prompts
from toon3d.generative.ldm3d import LDM3D, get_rgbd_vis
import mediapy

from diffusers.utils.torch_utils import is_compiled_module

from diffusers.loaders import LoraLoaderMixin
import wandb
from torchvision.transforms import v2

from nerfstudio.utils.colormaps import apply_depth_colormap
from toon3d.utils.depth_utils import depth_to_disparity

logger = get_logger(__name__)


def unet_attn_processors_state_dict(unet) -> Dict[str, torch.tensor]:
    r"""
    Returns:
        a state dict containing just the attention processor parameters.
    """
    attn_processors = unet.attn_processors

    attn_processors_state_dict = {}

    for attn_processor_key, attn_processor in attn_processors.items():
        for parameter_key, parameter in attn_processor.state_dict().items():
            attn_processors_state_dict[f"{attn_processor_key}.{parameter_key}"] = parameter

    return attn_processors_state_dict


def main(
    data_prefix: Path = Path("data/nerfstudio"),
    dataset: str = "bobs-burgers-dining",
    output_prefix: Path = Path("outputs"),
    gradient_accumulation_steps: int = 1,
    mixed_precision: Literal["no", "fp16", "bf16"] = "no",
    seed: Optional[int] = None,
    enable_xformers_memory_efficient_attention: bool = True,
    train_text_encoder: bool = True,
    checkpoints_total_limit: Optional[int] = None,
    prompt: Optional[str] = None,
    negative_prompt: Optional[str] = None,
    num_train_steps: int = 10000,
    train_batch_size: int = 1,
    lr: float = 1e-5,
    allow_tf32: bool = False,
    use_8bit_adam: bool = False,
    max_grad_norm: float = 1.0,
    adam_beta1: float = 0.9,
    adam_beta2: float = 0.999,
    adam_weight_decay: float = 1e-2,
    adam_epsilon: float = 1e-08,
    lr_scheduler: Literal[
        "linear", "cosine", "cosine_with_restarts", "polynomial", "constant", "constant_with_warmup"
    ] = "constant",
    lr_warmup_steps: int = 0,
    lr_num_cycles: float = 1,
    lr_power: float = 1.0,
    resume_from_checkpoint: bool = False,
    steps_per_checkpoint: int = 500,
    steps_per_val: int = 100,
    rank: int = 4,
):
    """Fine-tune a diffusion model on our data.

    Args:
        data_prefix: path to the data folder
        dataset: name of the dataset
        output_prefix: path to the output folder
        gradient_accumulation_steps: number of gradient accumulation steps
        mixed_precision: mixed precision training
        seed: random seed
        enable_xformers_memory_efficient_attention: whether to enable memory efficient attention
        train_text_encoder: whether to train the text encoder
        checkpoints_total_limit: maximum number of checkpoints to keep
        prompt: prompt to use
        negative_prompt: negative prompt to use
        num_train_steps: number of training steps to perform
        train_batch_size: batch size (per device) for training
        lr: learning rate
        allow_tf32: whether to allow TF32
        use_8bit_adam: whether to use 8-bit Adam
        max_grad_norm: maximum gradient norm
        adam_beta1: Adam beta 1
        adam_beta2: Adam beta 2
        adam_weight_decay: Adam weight decay
        adam_epsilon: Adam epsilon
        lr_scheduler: learning rate scheduler
        lr_warmpup_steps: number of warmup steps for the learning rate scheduler
        lr_num_cycles: number of hard resets of the lr in cosine_with_restarts scheduler
        lr_power: power factor of the polynomial scheduler
        resume_from_checkpoint: whether to resume from a checkpoint
        steps_per_checkpoint: number of steps between checkpoints
        steps_per_val: number of steps between validation runs
        rank: the dimension of the LoRA update matrices
    """

    fn_arguments = dict(locals())

    output_folder = output_prefix / dataset / "finetune" / datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_folder.mkdir(parents=True, exist_ok=True)
    logging_dir = output_folder / "logs"

    # get the prompts
    if prompt is not None:
        if negative_prompt is None:
            raise ValueError("If prompt is specified, negative_prompt must also be specified.")
    elif negative_prompt is not None:
        raise ValueError("If negative_prompt is specified, prompt must also be specified.")
    else:
        print("Getting prompts from config.")
        prompt, negative_prompt = get_prompts(dataset)

    accelerator_project_config = ProjectConfiguration(project_dir=output_folder, logging_dir=logging_dir)

    accelerator = Accelerator(
        gradient_accumulation_steps=gradient_accumulation_steps,
        mixed_precision=mixed_precision,
        log_with="wandb",
        project_config=accelerator_project_config,
    )

    # Make one log on every process with the configuration for debugging.
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )
    logger.info(accelerator.state, main_process_only=False)
    if accelerator.is_local_main_process:
        transformers.utils.logging.set_verbosity_warning()
        diffusers.utils.logging.set_verbosity_info()
    else:
        transformers.utils.logging.set_verbosity_error()
        diffusers.utils.logging.set_verbosity_error()

    if seed is not None:
        set_seed(seed)

    # For mixed precision training, cast non-trainable weights to the appropriate precision
    weight_dtype = (
        torch.float16
        if accelerator.mixed_precision == "fp16"
        else torch.bfloat16 if accelerator.mixed_precision == "bf16" else torch.float32
    )

    ldm3d = LDM3D(torch_dtype=weight_dtype, device=accelerator.device)
    # Load scheduler and models
    noise_scheduler = ldm3d.scheduler
    vae = ldm3d.auto_encoder
    text_encoder = ldm3d.text_encoder
    unet = ldm3d.unet
    # We only train the additional adapter LoRA layers
    vae.requires_grad_(False)
    text_encoder.requires_grad_(False)
    unet.requires_grad_(False)

    if enable_xformers_memory_efficient_attention:
        if not is_xformers_available():
            raise ValueError("xformers is not available. Make sure it is installed correctly")
        unet.enable_xformers_memory_efficient_attention()

    # now we will add new LoRA weights to the attention layers
    unet_lora_config = LoraConfig(
        r=rank,
        lora_alpha=rank,
        init_lora_weights="gaussian",
        target_modules=["to_k", "to_q", "to_v", "to_out.0", "add_k_proj", "add_v_proj"],
    )
    unet.add_adapter(unet_lora_config)

    # The text encoder comes from 🤗 transformers, we will also attach adapters to it.
    if train_text_encoder:
        text_lora_config = LoraConfig(
            r=rank,
            lora_alpha=rank,
            init_lora_weights="gaussian",
            target_modules=["q_proj", "k_proj", "v_proj", "out_proj"],
        )
        text_encoder.add_adapter(text_lora_config)

    def unwrap_model(model):
        model = accelerator.unwrap_model(model)
        model = model._orig_mod if is_compiled_module(model) else model
        return model

    def save_model_hook(models: List[torch.nn.Module], weights: List[Dict[str, torch.Tensor]], input_dir: str) -> None:
        """
        Custom saving & loading hooks so that `accelerator.save_state(...)` serializes in a nice format
        """
        print("Inside save model hook.")

        if accelerator.is_main_process:
            # there are only two options here. Either are just the unet attn processor layers
            # or there are the unet and text encoder atten layers
            unet_lora_layers_to_save = None
            text_encoder_lora_layers_to_save = None

            for model in models:
                if isinstance(model, type(unwrap_model(unet))):
                    unet_lora_layers_to_save = convert_state_dict_to_diffusers(get_peft_model_state_dict(model))
                elif isinstance(model, type(unwrap_model(text_encoder))):
                    text_encoder_lora_layers_to_save = convert_state_dict_to_diffusers(get_peft_model_state_dict(model))
                else:
                    raise ValueError(f"unexpected save model: {model.__class__}")

                # make sure to pop weight so that corresponding model is not saved again
                weights.pop()

            LoraLoaderMixin.save_lora_weights(
                input_dir,
                unet_lora_layers=unet_lora_layers_to_save,
                text_encoder_lora_layers=text_encoder_lora_layers_to_save,
            )

    def load_model_hook(models, input_dir):
        print("Inside load model hook.")

    accelerator.register_save_state_pre_hook(save_model_hook)
    accelerator.register_load_state_pre_hook(load_model_hook)

    # Enable TF32 for faster training on Ampere GPUs,
    # cf https://pytorch.org/docs/stable/notes/cuda.html#tensorfloat-32-tf32-on-ampere-devices
    if allow_tf32:
        raise NotImplementedError("TF32 is not yet supported.")

    # Use 8-bit Adam for lower memory usage or to fine-tune the model in 16GB GPUs
    if use_8bit_adam:
        raise NotImplementedError("8-bit Adam is not yet supported.")
    else:
        optimizer_class = torch.optim.AdamW

    # Optimizer creation
    params_to_optimize = list(filter(lambda p: p.requires_grad, unet.parameters()))
    if train_text_encoder:
        params_to_optimize = params_to_optimize + list(filter(lambda p: p.requires_grad, text_encoder.parameters()))

    optimizer = optimizer_class(
        params_to_optimize,
        lr=lr,
        betas=(adam_beta1, adam_beta2),
        weight_decay=adam_weight_decay,
        eps=adam_epsilon,
    )

    image_filenames = sorted(glob.glob(str(data_prefix / dataset / "images/*")))
    depth_filenames = sorted(glob.glob(str(data_prefix / dataset / "depths/*")))
    mask_filenames = sorted(glob.glob(str(data_prefix / dataset / "masks/*")))

    # load images, depths, and masks to cpu
    # TODO: use a dataset
    images = [torch.from_numpy(mediapy.read_image(filename)) / 255.0 for filename in image_filenames]
    depths = [torch.from_numpy(np.load(filename)) for filename in depth_filenames]
    masks = [torch.from_numpy(mediapy.read_image(filename))[..., None] / 255.0 for filename in mask_filenames]

    lr_scheduler = get_scheduler(
        lr_scheduler,
        optimizer=optimizer,
        num_warmup_steps=lr_warmup_steps * gradient_accumulation_steps,
        num_training_steps=num_train_steps * gradient_accumulation_steps,
        num_cycles=lr_num_cycles,
        power=lr_power,
    )

    # Prepare everything with our `accelerator`.
    if train_text_encoder:
        (
            unet,
            text_encoder,
            optimizer,
            lr_scheduler,
        ) = accelerator.prepare(unet, text_encoder, optimizer, lr_scheduler)
    else:
        unet, optimizer, lr_scheduler = accelerator.prepare(unet, optimizer, lr_scheduler)

    # We need to initialize the trackers we use, and also store our configuration.
    # The trackers initializes automatically on the main process.
    if accelerator.is_main_process:
        accelerator.init_trackers("toon3d-finetune", config=fn_arguments)

    # Train!
    total_batch_size = train_batch_size * accelerator.num_processes * gradient_accumulation_steps

    logger.info("***** Running training *****")
    logger.info(f"  Num examples = {len(images)}")
    logger.info(f"  Instantaneous batch size per device = {train_batch_size}")
    logger.info(f"  Total train batch size (w. parallel, distributed & accumulation) = {total_batch_size}")
    logger.info(f"  Gradient Accumulation steps = {gradient_accumulation_steps}")
    logger.info(f"  Total optimization steps = {num_train_steps}")

    # Potentially load in the weights and states from a previous save
    if resume_from_checkpoint:
        raise NotImplementedError("Resume from checkpoint is not yet supported.")

    # Only show the progress bar once on each machine.
    progress_bar = tqdm(
        range(num_train_steps),
        disable=not accelerator.is_local_main_process,
    )
    progress_bar.set_description("Steps")

    unet.train()
    if train_text_encoder:
        text_encoder.train()

    transforms = v2.Compose(
        [
            v2.RandomResizedCrop(size=(512, 512), antialias=True, scale=(0.8, 1.0)),
            v2.RandomHorizontalFlip(p=0.5),
        ]
    )

    for step in range(num_train_steps):
        # TODO: use a dataset
        # load images and depth
        image = images[step % len(images)][None].permute(0, 3, 1, 2)
        depth = depths[step % len(depths)][None].permute(0, 3, 1, 2)
        disparity = depth_to_disparity(depth)
        mask = masks[step % len(masks)][None].permute(0, 3, 1, 2)
        rgbdm = torch.cat([image, disparity, mask], dim=1).to(dtype=weight_dtype, device=unet.device)
        rgbdm = transforms(rgbdm)
        rgbd, m = rgbdm[:, :4], rgbdm[:, 4:]

        # TODO: figure out how to use the mask
        # rgbd = rgbd * m
        # uncomment to visualize the training batch (zeros where masked out)
        # rgbdm_vis = get_rgbd_vis(rgbd * m)
        # mediapy.write_image("finetune.png", rgbdm_vis[0].detach().cpu())

        # Skip steps until we reach the resumed step
        if resume_from_checkpoint:
            raise NotImplementedError("Resume from checkpoint is not yet supported.")

        with accelerator.accumulate(unet):
            # Convert images to latent space
            model_input = ldm3d.rgbd_to_latents(rgbd)

            # Sample noise that we'll add to the latents
            noise = torch.randn_like(model_input)
            bsz, channels, height, width = model_input.shape
            # Sample a random timestep for each image
            timesteps = torch.randint(
                0,
                noise_scheduler.config.num_train_timesteps,
                (bsz,),
                device=model_input.device,
            )
            timesteps = timesteps.long()

            # Add noise to the model input according to the noise magnitude at each timestep
            # (this is the forward diffusion process)
            latent_model_input = noise_scheduler.add_noise(model_input, noise, timesteps)

            # Get the text embedding for conditioning
            prompt_embeds = ldm3d.get_text_embeds(prompt, negative_prompt)
            prompt_embeds = prompt_embeds[0:1]
            encoder_hidden_states = prompt_embeds

            # Predict the noise residual
            model_pred = unet(latent_model_input, timesteps, encoder_hidden_states).sample

            # if model predicts variance, throw away the prediction. we will only train on the
            # simplified training objective. This means that all schedulers using the fine tuned
            # model must be configured to use one of the fixed variance variance types.
            if model_pred.shape[1] == 6:
                model_pred, _ = torch.chunk(model_pred, 2, dim=1)

            # Get the target for loss depending on the prediction type
            if noise_scheduler.config.prediction_type == "epsilon":
                target = noise
            elif noise_scheduler.config.prediction_type == "v_prediction":
                target = noise_scheduler.get_velocity(model_input, noise, timesteps)
            else:
                raise ValueError(f"Unknown prediction type {noise_scheduler.config.prediction_type}")

            # downscale m to match the model_pred, use nearest interpolation
            # m_down = F.interpolate(m, size=model_pred.shape[-2:], mode="nearest")

            loss = F.mse_loss(model_pred.float(), target.float(), reduction="mean")

            accelerator.backward(loss)
            if accelerator.sync_gradients:
                accelerator.clip_grad_norm_(params_to_optimize, max_grad_norm)
            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()

        # Checks if the accelerator has performed an optimization step behind the scenes
        if accelerator.sync_gradients:
            progress_bar.update(1)

            if accelerator.is_main_process:
                if step % steps_per_checkpoint == 0:
                    print("Saving checkpoint.")
                    save_path = os.path.join(output_folder, f"checkpoint-{step:06d}")
                    accelerator.save_state(save_path)
                    logger.info(f"Saved state to {save_path}")

        logs = {
            "loss": loss.detach().item(),
            "lr": lr_scheduler.get_last_lr()[0],
        }
        progress_bar.set_postfix(**logs)
        accelerator.log(logs, step=step)

        if accelerator.is_main_process:
            if step % steps_per_val == 0:
                print("Running validation.")

                rgbd = ldm3d.prompt_to_rgbd(prompt, negative_prompt)
                rgbd_vis = get_rgbd_vis(rgbd)

                for tracker in accelerator.trackers:
                    if tracker.name == "wandb":
                        # first arg to wandb.Image should be shape [H, W, 3]
                        tracker.log(
                            {"validation": [wandb.Image(rgbd_vis.detach().cpu().numpy(), caption="validation image 0")]}
                        )

    # Save the lora layers
    accelerator.wait_for_everyone()
    if accelerator.is_main_process:
        unet = unwrap_model(unet)
        unet = unet.to(torch.float32)

        unet_lora_state_dict = convert_state_dict_to_diffusers(get_peft_model_state_dict(unet))

        if train_text_encoder:
            text_encoder = unwrap_model(text_encoder)
            text_encoder_state_dict = convert_state_dict_to_diffusers(get_peft_model_state_dict(text_encoder))
        else:
            text_encoder_state_dict = None

        LoraLoaderMixin.save_lora_weights(
            save_directory=output_folder,
            unet_lora_layers=unet_lora_state_dict,
            text_encoder_lora_layers=text_encoder_state_dict,
        )

    accelerator.end_training()


def entrypoint():
    """Entrypoint for use with pyproject scripts."""
    tyro.extras.set_accent_color("bright_yellow")
    tyro.cli(main)


if __name__ == "__main__":
    entrypoint()
