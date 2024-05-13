"""
Test fine-tune functionality
"""

from toon3d.scripts.finetune import main as finetune_main
from pathlib import Path


def test_finetune():
    """test run finetune script"""
    finetune_main(num_train_steps=10, steps_per_checkpoint=5, steps_per_val=2, output_prefix=Path("outputs-tests"))


if __name__ == "__main__":
    test_finetune()
