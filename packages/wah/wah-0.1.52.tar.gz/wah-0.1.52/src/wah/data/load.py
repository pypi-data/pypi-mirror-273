import random

from torch.utils.data import Subset

from ..typing import (
    Config,
    DataLoader,
    Dataset,
    Optional,
)
from .transforms import CollateFunction

__all__ = [
    "load_dataloader",
    "portion_dataset",
]


def load_dataloader(
    dataset: Dataset,
    config: Config,
    train: Optional[bool] = False,
) -> DataLoader:
    collate_fn = (
        CollateFunction(
            mixup_alpha=config["mixup_alpha"],
            cutmix_alpha=config["cutmix_alpha"],
            num_classes=config["num_classes"],
        )
        if train
        else None
    )

    return DataLoader(
        dataset=dataset,
        batch_size=config["batch_size"],
        shuffle=True if train else False,
        num_workers=config["num_workers"],
        persistent_workers=True if config["num_workers"] > 0 else False,
        collate_fn=collate_fn,
    )


def portion_dataset(
    dataset: Dataset,
    portion: float,
    balanced: Optional[bool] = True,
    random_sample: Optional[bool] = False,
) -> Subset:
    assert 0 < portion <= 1, f"Expected 0 < portion <= 1, got {portion}"

    if balanced:
        assert hasattr(
            dataset, "targets"
        ), f"Unable to create a balanced dataset as there are no targets in the dataset."

        targets = dataset.targets
        classes = list(set(targets))

        indices = []

        for c in classes:
            c_indices = [i for i, target in enumerate(targets) if target == c]
            num_c = int(len(c_indices) * portion)

            if random_sample:
                c_indices = random.sample(c_indices, num_c)

            else:
                c_indices = c_indices[:num_c]

            indices += c_indices

    else:
        num_data = int(len(dataset) * portion)

        if random_sample:
            indices = random.sample([i for i in range(len(dataset))], num_data)

        else:
            indices = [i for i in range(len(dataset))][:num_data]

    return Subset(dataset, indices)
