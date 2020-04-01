"""A set of utility functions for Valiant config."""
from collections import ChainMap
from pathlib import Path
from typing import Any
from typing import ChainMap as ChainMapType
from typing import Mapping, Optional, Tuple

from valiant.config import Config, ConfigBuilder
from valiant.config.builder import ConfigMap


def get_valiant_base_config() -> ConfigMap:
    """Returns a config map with the Valiant defaults.

    This method MUST build out a complete configuration for Valiant

    Returns:
        A default Config instance.
    """
    from os import path
    from pathlib import Path
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
                    "file": path.join(
                        dirs.user_cache_dir, f"{app}-{version}-requests-cache",
                    ),
                    "backend": "sqlite",
                    "expire_after": 86400,
                },
                "repository_configurations": {"pypi": PyPiRepository.get_pypi_config()},
                "logging_configuration_file": None,
                "logging_configuration": setup_logging_configuration(
                    handlers={
                        "default": {
                            "level": "INFO",
                            "formatter": "standard",
                            "class": "logging.handlers.RotatingFileHandler",
                            "filename": Path(dirs.user_log_dir, "valiant.log"),
                            "maxBytes": 500000,
                            "backupCount": 3,
                        }
                    },
                ),
            }
        }
    }


def generate_valiant_config_from_map(config: ChainMapType) -> Config:
    """Create a Config instance from a dictionary rendition.

    Args:
        config: A dictionary that aligns with the init params for Config

    Returns:
        A Config instance ready to go
    """

    def _valiant_config_in_mapping(cfg: Mapping) -> bool:
        if "tool" in cfg:
            if "valiant" in cfg["tool"]:
                return True
        return False

    def _extract_valiant_configuration_maps(
        map: ChainMap,
    ) -> Tuple[Mapping[str, Any], Mapping[str, Any]]:
        metadata = map["_builder_metadata"]
        valiant_config: Mapping[str, Any] = ChainMap(
            *[m["tool"]["valiant"] for m in map.maps if _valiant_config_in_mapping(m)]
        )
        return (metadata, valiant_config)

    metadata, valiant_conf = _extract_valiant_configuration_maps(config)

    log_config_file: Optional[Path] = None
    if "logging_configuration_file" in valiant_conf:
        if valiant_conf["logging_configuration_file"]:
            log_config_file = Path(valiant_conf["logging_configuration_file"])

    return Config(
        configuration_dir=Path(valiant_conf["configuration_dir"]),
        cache_dir=Path(valiant_conf["cache_dir"]),
        log_dir=Path(valiant_conf["log_dir"]),
        default_repository=valiant_conf["default_repository"],
        default_reports=set(valiant_conf["default_reports"]),
        repository_configurations=valiant_conf["repository_configurations"],
        requests_cache=valiant_conf["requests_cache"],
        logging_configuration=valiant_conf["logging_configuration"],
        logging_configuration_file=log_config_file,
        metadata=metadata,
    )


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
