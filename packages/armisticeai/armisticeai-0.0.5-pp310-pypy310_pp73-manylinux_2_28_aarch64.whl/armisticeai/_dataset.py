from typing import List
from datasets import (
    load_dataset as load_dataset_hf,
    load_from_disk,
    Dataset,
    load_dataset_builder,
)
import random
from typing import List, Tuple
import os
from ._exceptions import ArmisticeAIError


def split_dataset(ds: Dataset, percentages: list) -> list:
    total_size = len(ds)
    split_sizes = [int(p * total_size) for p in percentages]

    # Adjust the last split size to account for rounding errors
    split_sizes[-1] = total_size - sum(split_sizes[:-1])

    # Shuffle indices to ensure random splits
    random.seed(42)
    indices = list(range(total_size))
    random.shuffle(indices)

    split_datasets = []
    curr_idx = 0
    for size in split_sizes:
        split_indices = indices[curr_idx : curr_idx + size]
        split_dataset = ds.select(split_indices)
        split_datasets.append(split_dataset)
        curr_idx += size

    return split_datasets


class ArmisticeDataset:
    def __init__(self, name: str):
        self.name = name
        self.trainset, self.testset = self._load_dataset()
        self.labels = self._load_labels()
        self.label2id, self.id2label = self._load_label_id_map()

    def _load_labels(self) -> List[str]:
        return self.trainset.features["label"].names

    def _load_dataset(self) -> Tuple[Dataset, Dataset]:
        if os.path.isdir(self.name):
            dataset = load_from_disk(self.name)
        else:
            try:
                load_dataset_builder(self.name, token=True)
            except:
                raise ArmisticeAIError(
                    f"Failed to load dataset from HuggingFace with identifier '{self.name}'"
                )
        dataset = load_dataset_hf(self.name, token=True)
        return dataset["train"], dataset["validation"]

    def _load_label_id_map(self):
        label2id, id2label = dict(), dict()
        for i, label in enumerate(self.labels):
            label2id[label] = i
            id2label[i] = label
        return label2id, id2label
