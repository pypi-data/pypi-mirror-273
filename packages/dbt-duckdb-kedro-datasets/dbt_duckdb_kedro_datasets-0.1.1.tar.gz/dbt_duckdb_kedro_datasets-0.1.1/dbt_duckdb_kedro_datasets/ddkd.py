from typing import Any
from typing import Dict
from dbt.adapters.duckdb.plugins import BasePlugin
from dbt.adapters.duckdb.utils import SourceConfig, TargetConfig
from dbt.adapters.duckdb.plugins import pd_utils
import importlib
import os


def _get_dataset_loader(config: SourceConfig):
    # source_config[`type`] is of form pandas.CSVDataset
    module_names = config["type"].split(
        ".",
    )[:-1]
    module_name = ".".join(module_names)
    package_name = config["type"].split(
        ".",
    )[-1]
    # `dataset_loader` should now be equal to something like `CSVDataset`
    dataset_module = importlib.import_module(name=f"kedro_datasets.{module_name}")
    dataset_loader = getattr(dataset_module, package_name)
    return dataset_loader


class Plugin(BasePlugin):
    def initialize(
        self,
        plugin_config: Dict[str, Any],
    ):
        pass

    def store(
        self,
        target_config: TargetConfig,
    ):
        kedro_config = target_config.config.get("kedro_yml_config")
        dataset_loader = _get_dataset_loader(kedro_config)
        del kedro_config["type"]
        df = pd_utils.target_to_df(target_config)
        dataset_loader(**kedro_config).save(df)
        # duck-dbt create a parquet file when materialize is set to `external`
        # this deletes that file after we have used kedro-datasets to save the file
        os.remove(target_config.location.path)

    def load(self, source_config: SourceConfig):
        print(source_config)
        dataset_loader = _get_dataset_loader(source_config.meta)
        del source_config.meta["type"]
        del source_config.meta["plugin"]
        dataset = dataset_loader(**source_config.meta)
        return dataset.load()
