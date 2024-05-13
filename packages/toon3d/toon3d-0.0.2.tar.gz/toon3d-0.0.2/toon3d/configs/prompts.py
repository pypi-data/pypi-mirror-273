"""
A file to store the information about prompts.
"""

from typing import Tuple
from nerfstudio.utils.rich_utils import CONSOLE

# A dictionary to store the information for prompts for each dataset.
dataset_to_prompts = {
    "bobs-burgers-dining": {"positive": "a photo from bob's burgers restaurant"},
    "family-guy-house": {"positive": "a photo of the family guy house"},
}
default_negative = (
    "worst quality, normal quality, low quality, low res, blurry, text, watermark, "
    "logo, banner, extra digits, cropped, jpeg artifacts, signature, username, error, "
    "duplicate, ugly, monochrome, horror, geometry, mutation, disgusting"
)


def get_prompts(dataset: str) -> Tuple[str, str]:
    """
    A function to get the prompts for a given dataset.

    Args:
        dataset: The name of the dataset.
        allow_default_positive: Whether to allow the default positive prompt.

    Returns:
        The positive and negative prompts.
    """
    if dataset not in dataset_to_prompts:
        raise ValueError(f"Dataset '{dataset}' not found in the prompts. Please add it to the prompts in the config.")
    prompts = dataset_to_prompts[dataset]
    if "negative" not in prompts:
        prompts["negative"] = default_negative
    prompt, negative_prompt = prompts["positive"], prompts["negative"]
    CONSOLE.print(f'[bold green]Prompt: "{prompt}"')
    CONSOLE.print(f'[bold green]Negative Prompt: "{negative_prompt}"')
    return prompt, negative_prompt
