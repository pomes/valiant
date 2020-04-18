"""A set of utility functions for Valiant config.

Copyright (c) 2020 The Valiant Authors

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from collections import ChainMap
from collections.abc import Mapping as MappingType
from pathlib import Path
from typing import Any
from typing import ChainMap as ChainMapType
from typing import Dict, List, Mapping, Optional, Set, Tuple, Union

from valiant.config import Config, ConfigBuilder
from valiant.config.builder import ConfigMap
from valiant.repositories import RepositoryConfiguration


def get_valiant_base_config() -> ConfigMap:
    """Returns a config map with the Valiant defaults.

    This method MUST build out a complete configuration for Valiant

    Returns:
        A default Config instance.
    """
    from valiant import Valiant
    from valiant.log import setup_logging_configuration
    from valiant.repositories.pypi import PyPiRepository
    from appdirs import AppDirs

    vendor, app, version = Valiant.application_details()
    dirs = AppDirs(appname=app, appauthor=vendor, version=version)

    return {
        "tool": {
            "valiant": {
                "configuration_dir": dirs.user_config_dir,
                "cache_dir": dirs.user_cache_dir,
                "log_dir": dirs.user_log_dir,
                "default_repository": "pypi",
                "default_reports": ["basic", "spdx", "safety"],
                "requests_cache": {
                    "file": f"$cache_dir/{app}-{version}-requests-cache",
                    "backend": "sqlite",
                    "expire_after": 86400,
                },
                "repository_configurations": {"pypi": PyPiRepository.get_pypi_config()},
                "local-plugins": {"paths": [], "valiant.reports": {}},
                "logging_configuration_file": None,
                "logging_configuration": setup_logging_configuration(
                    handlers={
                        "default": {
                            "level": "INFO",
                            "formatter": "standard",
                            "class": "logging.handlers.RotatingFileHandler",
                            "filename": "$log_dir/valiant.log",
                            "maxBytes": 500000,
                            "backupCount": 3,
                        }
                    },
                ),
            }
        }
    }


class ConfigMapBuilder:
    """Tries to simplify the building of a Config instance from a Mapping."""

    def __init__(self) -> None:
        """Initializer."""
        self.configuration_dir: Path
        self.cache_dir: Path
        self.log_dir: Path
        self.default_repository: str
        self.repository_configurations: Mapping[str, RepositoryConfiguration]
        self.default_reports: Set[str]
        self.requests_cache: Mapping[str, Union[str, int]]
        self.logging_configuration: Mapping
        self.logging_configuration_file: Optional[Path]
        self.local_plugin_paths: List[str]
        self.local_report_plugins: Mapping[str, str]
        self.metadata: Optional[Mapping[str, Any]]

    def build(self) -> Config:
        """Build the instance."""  # noqa:DAR201
        return Config(
            configuration_dir=self.configuration_dir,
            cache_dir=self.cache_dir,
            log_dir=self.log_dir,
            default_repository=self.default_repository,
            default_reports=self.default_reports,
            repository_configurations=self.repository_configurations,
            requests_cache=self.requests_cache,
            logging_configuration=self.logging_configuration,
            logging_configuration_file=self.logging_configuration_file,
            local_plugin_paths=self.local_plugin_paths,
            local_report_plugins=self.local_report_plugins,
            metadata=self.metadata,
        )

    @staticmethod
    def _valiant_config_in_mapping(cfg: Mapping) -> bool:
        if "tool" in cfg:
            if "valiant" in cfg["tool"]:
                return True
        return False

    @staticmethod
    def _extract_valiant_configuration_maps(
        map: ChainMap,
    ) -> Tuple[Mapping[str, Any], Mapping[str, Any]]:
        metadata = map["_builder_metadata"]
        valiant_config: Mapping[str, Any] = ChainMap(
            *[
                m["tool"]["valiant"]
                for m in map.maps
                if ConfigMapBuilder._valiant_config_in_mapping(m)
            ]
        )
        return (metadata, valiant_config)

    @staticmethod
    def _extract_repo_confs(
        confs: Mapping[str, Union[Mapping, RepositoryConfiguration]]
    ) -> Mapping[str, RepositoryConfiguration]:
        from typing import cast

        repo_confs: Dict[str, RepositoryConfiguration] = {}
        for k, v in confs.items():
            if type(v) is RepositoryConfiguration:
                repo_confs[k] = cast(RepositoryConfiguration, v)
            elif issubclass(type(v), MappingType):
                repo_confs[k] = RepositoryConfiguration(**(cast(Mapping, v)))

        return repo_confs

    @staticmethod
    def _extract_plugin_conf(
        config: Mapping[str, Any],
    ) -> Tuple[List[str], Mapping[str, str]]:
        local_plugin_paths = []
        if "paths" in config["local-plugins"]:
            local_plugin_paths = config["local-plugins"]["paths"]

        local_report_plugins = {}
        if "valiant.report" in config["local-plugins"]:
            local_report_plugins = config["local-plugins"]["valiant.report"]

        return local_plugin_paths, local_report_plugins

    @staticmethod
    def _extract_log_configuration(
        config: Mapping[str, Any],
    ) -> Tuple[Optional[Path], Mapping]:

        if "logging_configuration_file" in config:
            if config["logging_configuration_file"]:
                return Path(config["logging_configuration_file"]), {}

        return None, config["logging_configuration"]

    @staticmethod
    def generate_valiant_config_from_map(config: ChainMapType) -> Config:
        """Create a Config instance from a dictionary rendition.

        Args:
            config: A dictionary that aligns with the init params for Config

        Returns:
            A Config instance ready to go
        """
        builder = ConfigMapBuilder()

        metadata, valiant_conf = ConfigMapBuilder._extract_valiant_configuration_maps(
            config
        )
        builder.metadata = metadata

        builder.configuration_dir = Path(valiant_conf["configuration_dir"])
        builder.cache_dir = Path(valiant_conf["cache_dir"])
        builder.log_dir = Path(valiant_conf["log_dir"])
        builder.default_repository = valiant_conf["default_repository"]
        builder.default_reports = set(valiant_conf["default_reports"])
        builder.repository_configurations = ConfigMapBuilder._extract_repo_confs(
            valiant_conf["repository_configurations"]
        )
        builder.requests_cache = valiant_conf["requests_cache"]

        (
            builder.logging_configuration_file,
            builder.logging_configuration,
        ) = ConfigMapBuilder._extract_log_configuration(valiant_conf)

        (
            builder.local_plugin_paths,
            builder.local_report_plugins,
        ) = ConfigMapBuilder._extract_plugin_conf(valiant_conf)

        return builder.build()


def valiant_config_filter(d: ConfigMap) -> ConfigMap:
    """Filter out all no tool.valiant entries.

    Used by ConfigBuilder
    # noqa: DAR101
    # noqa: DAR201
    """
    from valiant import Valiant

    _, app_name, _ = Valiant.application_details()

    if "tool" not in d:
        return {}

    if app_name not in d["tool"]:
        return {}

    return {"tool": {app_name: d["tool"][app_name]}}


def create_valiant_builder(
    include_pyproject: bool = True,
    include_user_config: bool = True,
    include_site_config: bool = True,
) -> ConfigBuilder:
    """Create a config builder ready for Valiant.

    Args:
        include_pyproject: True if the local pyproject.toml file is to be read
        include_user_config: True if the user's config directory is to be used
        include_site_config: True if the system's config directory is to be used

    Returns:
        A ConfigBuilder instance readied with the expected config sources
    """
    from valiant import Valiant

    vendor, app, version = Valiant.application_details()

    return ConfigBuilder.create_default_builder(
        initial_data=get_valiant_base_config(),
        vendor=vendor,
        app=app,
        version=version,
        include_pyproject=include_pyproject,
        include_user_config=include_user_config,
        include_site_config=include_site_config,
        filter=valiant_config_filter,
    )
