"""Tests for the Valiant Config class."""
import os

from pathlib import Path

import pytest

from valiant.config import Config, ConfigBuilder
from valiant.config.source import MappingSource
from valiant.repositories import RepositoryConfiguration
from valiant.repositories.pypi import PyPiRepository


PYPI_CONFIG = PyPiRepository.get_pypi_config()


@pytest.fixture(scope="function")
def config_builder(tmp_path: Path) -> ConfigBuilder:
    """Create a builder ready for test runs.

    Returns:
        ConfigBuilder instance.
    """
    from valiant.config.util import create_valiant_builder

    builder = create_valiant_builder(
        include_pyproject=False, include_user_config=False, include_site_config=False
    )
    builder.add_source(
        MappingSource(
            {
                "tool": {
                    "valiant": {
                        "configuration_dir": os.path.join(tmp_path, "etc"),
                        "cache_dir": os.path.join(tmp_path, "var"),
                        "log_dir": os.path.join(tmp_path, "log"),
                    }
                }
            }
        )
    )
    return builder


def get_config_instance(builder: ConfigBuilder) -> Config:
    """Helper function to setup a Config instance from the builder.

    # noqa:DAR201
    # noqa:DAR401
    """
    from valiant.config.util import ConfigMapBuilder

    conf_map = builder.build()

    if conf_map:
        return ConfigMapBuilder.generate_valiant_config_from_map(conf_map)
    else:
        raise ValueError("Failed to generate config instance.")


def test_empty_config() -> None:
    """Checks config with no initial settings."""
    with pytest.raises(TypeError):
        Config()  # type: ignore


def test_basic_config(tmp_path: Path, config_builder: ConfigBuilder) -> None:
    """Basic config test."""
    c = get_config_instance(config_builder)

    assert c.configuration_dir == Path(os.path.join(tmp_path, "etc"))
    assert c.cache_dir == Path(os.path.join(tmp_path, "var"))
    assert c.log_dir == Path(os.path.join(tmp_path, "log"))
    assert c.default_repository == "pypi"
    assert c.default_reports == set(["basic", "safety", "spdx"])


# def test_no_repo_config(config_builder: ConfigBuilder) -> None:
#    """Expect failure when there are no repository_configurations."""
#    config_builder.add_source(
#        DictionarySource({"tool": {"valiant": {"repository_configurations": {}}}})
#    )
#    with pytest.raises(ValueError):
#        get_config_instance(config_builder)


# def test_no_default_repo(config_builder: ConfigBuilder) -> None:  # noqa:ANN001
#    """Expect failure when the default_repo isn't listed in repository_configurations."""
#    config_builder.add_source(
#        DictionarySource({"tool": {"valiant": {"default_repository": "random_repo"}}})
#    )
#    with pytest.raises(ValueError):
#        get_config_instance(config_builder)

"""Start: Tests for Config.prepare_repository_configurations"""


def test_prepare_repository_configurations_auto_default() -> None:
    """Check error for prepare_repository_configurations with no default_repo."""
    default, configs = Config.prepare_repository_configurations(
        repository_configurations=[
            RepositoryConfiguration(name="test", base_url="https://www.example.com"),
        ],
        default_repository=None,
    )

    assert default == "test"


def test_multiple_repos_bad_default() -> None:
    """Check error for prepare_repository_configurations with a missing default_repo."""
    with pytest.raises(ValueError):
        Config.prepare_repository_configurations(
            repository_configurations=[
                RepositoryConfiguration(
                    name="test", base_url="https://www.example.com"
                ),
                RepositoryConfiguration(
                    name="test2", base_url="https://www.differentexample.com"
                ),
            ],
            default_repository="otter",
        )


def test_bad_config_repeated_repos() -> None:
    """Check error for prepare_repository_configurations with repeated repository entries."""
    with pytest.raises(ValueError):
        Config.prepare_repository_configurations(
            repository_configurations=[
                RepositoryConfiguration(
                    name="test", base_url="https://www.example.com"
                ),
                RepositoryConfiguration(
                    name="test", base_url="https://www.differentexample.com"
                ),
            ],
            default_repository="test",
        )


def test_multiple_repos_no_default() -> None:
    """Check error for prepare_repository_configurations with no default_repo."""
    with pytest.raises(ValueError):
        Config.prepare_repository_configurations(
            repository_configurations=[
                RepositoryConfiguration(
                    name="test", base_url="https://www.example.com"
                ),
                RepositoryConfiguration(
                    name="test2", base_url="https://www.differentexample.com"
                ),
            ],
            default_repository=None,
        )


"""End: Tests for Config.prepare_repository_configurations"""
