from torchvision.transforms import v2
import torch
from transformers import AutoImageProcessor
from datasets import Dataset
from typing import Tuple


def preprocess(
    image_processor: AutoImageProcessor, trainset: Dataset, testset: Dataset
) -> Tuple[Dataset, Dataset]:
    # TODO: Isolate the applied transforms so they can be applied from the server
    _transforms = v2.Compose(
        [
            v2.RandomResizedCrop(
                (image_processor.size["height"], image_processor.size["width"])
            ),
            v2.ToImage(),
            v2.ToDtype(torch.float32, scale=True),
            v2.Normalize(
                mean=image_processor.image_mean, std=image_processor.image_std
            ),
        ]
    )

    def transforms(examples):
        examples["pixel_values"] = [
            _transforms(img.convert("RGB")) for img in examples["image"]
        ]
        del examples["image"]
        return examples

    return trainset.with_transform(transforms), testset.with_transform(transforms)
