import logging
from abc import abstractmethod
from pathlib import Path
from typing import Any, Mapping, Sequence

from datasets import ClassLabel, Dataset, DatasetDict, load_dataset

from latentis.data import DATA_DIR
from latentis.data.dataset import DataType, Feature, FeatureMapping, FeatureProperty, LatentisDataset

pylogger = logging.getLogger(__name__)


def map_features(dataset: Dataset, *feature_mappings: FeatureMapping):
    dataset = dataset.map(
        lambda *source_col_vals: {
            target_col: source_col_val
            for source_col_val, target_col in zip(
                source_col_vals, [feature_mapping.target_col for feature_mapping in feature_mappings]
            )
        },
        batched=True,
        input_columns=[feature_mapping.source_col for feature_mapping in feature_mappings],
    )

    # for feature_mapping in feature_mappings:
    #     dataset = dataset.cast_column(
    #         feature_mapping.target_col,
    #         feature=dataset.features[feature_mapping.source_col].dtype,
    #     )

    return dataset


_RANDOM_SEED: int = 42
_ID_COLUMN: str = "sample_id"


class DataProcessor:
    def __init__(
        self,
        load_dataset_params: Mapping[str, Any],
        features: Sequence[Feature],
        metadata={},
        id_column: str = _ID_COLUMN,
    ):
        self.load_dataset_params = load_dataset_params
        self.features = features
        self.metadata = metadata
        self.id_column = id_column

    @abstractmethod
    def _process(self, dataset: DatasetDict) -> DatasetDict:
        raise NotImplementedError

    def process(self, dataset_name: str = None, perc: float = 1, parent_dir: Path = DATA_DIR) -> LatentisDataset:
        hf_dataset: DatasetDict = load_dataset(**self.load_dataset_params)
        dataset_name: str = dataset_name or list(hf_dataset.values())[0].info.dataset_name

        # Select a random subset, if needed
        if perc != 1:
            hf_dataset = DatasetDict(
                {
                    split: hf_dataset[split]
                    .shuffle(seed=_RANDOM_SEED)
                    .select(list(range(int(len(hf_dataset[split]) * perc))))
                    for split in hf_dataset.keys()
                }
            )

        start_columns = {col for cols in hf_dataset.column_names.values() for col in cols}
        core_columns = {feature.col_name for feature in self.features}

        hf_dataset: DatasetDict = self._process(dataset=hf_dataset)

        hf_dataset = hf_dataset.remove_columns([col for col in start_columns if col not in core_columns])

        hf_dataset = hf_dataset.map(
            lambda _, index: {self.id_column: index},
            with_indices=True,
        )

        processed_dataset = LatentisDataset(
            name=dataset_name,
            perc=perc,
            hf_dataset=hf_dataset,
            id_column=self.id_column,
            features=self.features,
            parent_dir=parent_dir,
        )

        return processed_dataset


class DBPedia14(DataProcessor):
    def __init__(self):
        super().__init__(
            load_dataset_params=dict(path="dbpedia_14"),
            features=[
                Feature(col_name="x", data_type=DataType.TEXT, properties={FeatureProperty.LANGUAGE: "en"}),
                Feature(col_name="y", data_type=DataType.LABEL),
            ],
        )

    def _process(self, dataset: DatasetDict) -> LatentisDataset:
        dataset = dataset.map(
            lambda title, content: {
                "x": [title + ". " + content.strip('"').strip() for title, content in zip(title, content)]
            },
            input_columns=["title", "content"],
            batched=True,
        )
        dataset = map_features(dataset, FeatureMapping(source_col="label", target_col="y"))

        return dataset


class TREC(DataProcessor):
    def __init__(self):
        super().__init__(
            load_dataset_params=dict(path="trec"),
            features=[
                Feature(col_name="text", data_type=DataType.TEXT, properties={FeatureProperty.LANGUAGE: "en"}),
                Feature(
                    col_name="coarse_label",
                    data_type=DataType.LABEL,
                    properties={FeatureProperty.FINE_GRAINED: False},
                ),
                Feature(
                    col_name="fine_label",
                    data_type=DataType.LABEL,
                    properties={FeatureProperty.FINE_GRAINED: True},
                ),
            ],
        )

    def _process(self, dataset: DatasetDict) -> DatasetDict:
        return dataset


class AGNews(DataProcessor):
    def __init__(self):
        super().__init__(
            load_dataset_params=dict(path="ag_news"),
            features=[
                Feature(col_name="text", data_type=DataType.TEXT, properties={FeatureProperty.LANGUAGE: "en"}),
                Feature(col_name="label", data_type=DataType.LABEL),
            ],
        )

    def _process(self, dataset: DatasetDict) -> DatasetDict:
        dataset = dataset.cast_column(
            "label",
            ClassLabel(
                num_classes=len(set(dataset["train"]["label"])),
                names=list(set(dataset["train"]["label"])),
            ),
        )

        return dataset


class IMDB(DataProcessor):
    def __init__(self):
        super().__init__(
            load_dataset_params=dict(path="imdb"),
            features=[
                Feature(col_name="text", data_type=DataType.TEXT, properties={FeatureProperty.LANGUAGE: "en"}),
                Feature(col_name="label", data_type=DataType.LABEL),
            ],
        )

    def _process(self, dataset: DatasetDict) -> DatasetDict:
        del dataset["unsupervised"]
        fit_data = dataset["train"].train_test_split(test_size=0.1, seed=_RANDOM_SEED)
        dataset["train"] = fit_data["train"]
        dataset["val"] = fit_data["test"]

        dataset = dataset.cast_column(
            "label",
            ClassLabel(
                num_classes=len(set(dataset["train"]["label"])),
                names=list(set(dataset["train"]["label"])),
            ),
        )

        return dataset


class MNIST(DataProcessor):
    def __init__(self):
        super().__init__(
            load_dataset_params=dict(path="mnist"),
            features=[
                Feature(col_name="image", data_type=DataType.IMAGE),
                Feature(col_name="label", data_type=DataType.LABEL),
            ],
        )

    def _process(self, dataset: DatasetDict) -> DatasetDict:
        # transforms = Compose(
        #     [
        #         ToTensor(),
        #     ]
        # )

        # dataset = dataset.map(
        #     lambda images: {"image": [transforms(image.convert("RGB")) for image in images]},
        #     input_columns=["image"],
        #     batched=True,
        # )
        # dataset = dataset.with_format("torch", columns=["image"])

        dataset = dataset.cast_column(
            "label",
            ClassLabel(
                num_classes=len(set(dataset["train"]["label"])),
                names=list(set(dataset["train"]["label"])),
            ),
        )

        return dataset


class CIFAR10(DataProcessor):
    def __init__(self):
        super().__init__(
            load_dataset_params=dict(path="cifar10"),
            features=[
                Feature(col_name="image", data_type=DataType.IMAGE),
                Feature(col_name="label", data_type=DataType.LABEL),
            ],
        )

    def _process(self, dataset: DatasetDict) -> DatasetDict:
        # transforms = Compose(
        #     [
        #         ToTensor(),
        #     ]
        # )

        # dataset = dataset.map(
        #     lambda images: {"image": [transforms(image.convert("RGB")) for image in images]},
        #     input_columns=["img"],
        #     batched=True,
        # )
        # dataset = dataset.with_format("torch", columns=["image"])
        dataset = dataset.rename_column("img", "image")

        dataset = dataset.cast_column(
            "label",
            ClassLabel(
                num_classes=len(set(dataset["train"]["label"])),
                names=list(set(dataset["train"]["label"])),
            ),
        )

        return dataset


class CIFAR100(DataProcessor):
    def __init__(self):
        super().__init__(
            load_dataset_params=dict(path="cifar100"),
            features=[
                Feature(col_name="image", data_type=DataType.IMAGE),
                Feature(
                    col_name="fine_label",
                    data_type=DataType.LABEL,
                    properties={FeatureProperty.FINE_GRAINED: True},
                ),
                Feature(
                    col_name="coarse_label",
                    data_type=DataType.LABEL,
                    properties={FeatureProperty.FINE_GRAINED: False},
                ),
            ],
        )

    def _process(self, dataset: DatasetDict) -> DatasetDict:
        # transforms = Compose(
        #     [
        #         ToTensor(),
        #     ]
        # )

        # dataset = dataset.map(
        #     lambda images: {"image": [transforms(image.convert("RGB")) for image in images]},
        #     input_columns=["img"],
        #     batched=True,
        # )
        # dataset = dataset.with_format("torch", columns=["image"])
        dataset = dataset.rename_column("img", "image")

        for label in ("coarse_label", "fine_label"):
            dataset = dataset.cast_column(
                label,
                ClassLabel(
                    num_classes=len(set(dataset["train"][label])),
                    names=list(set(dataset["train"][label])),
                ),
            )

        return dataset


class FashionMNIST(DataProcessor):
    def __init__(self):
        super().__init__(
            load_dataset_params=dict(path="fashion_mnist"),
            features=[
                Feature(col_name="image", data_type=DataType.IMAGE),
                Feature(col_name="label", data_type=DataType.LABEL),
            ],
        )

    def _process(self, dataset: DatasetDict) -> DatasetDict:
        # transforms = Compose(
        #     [
        #         ToTensor(),
        #     ]
        # )

        # dataset = dataset.map(
        #     lambda images: {"image": [transforms(image.convert("RGB")) for image in images]},
        #     input_columns=["image"],
        #     batched=True,
        # )

        # dataset = dataset.with_format("torch", columns=["image"])

        dataset = dataset.cast_column(
            "label",
            ClassLabel(
                num_classes=len(set(dataset["train"]["label"])),
                names=list(set(dataset["train"]["label"])),
            ),
        )

        return dataset


if __name__ == "__main__":
    latentis_dataset = IMDB().process(
        perc=0.05,
    )

    latentis_dataset.save_to_disk()
