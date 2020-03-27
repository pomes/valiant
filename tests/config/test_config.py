"""Tests for the Valiant Config class."""
from pathlib import Path

import pytest

from valiant.config import Config
from valiant.config.config import _load_default_config
from valiant.reports import ReportProviderConfiguration
from valiant.repositories import RepositoryConfiguration
from valiant.repositories.pypi import PyPiRepository


PYPI_CONFIG = PyPiRepository.get_pypi_config()


def test_default_config() -> None:
    """Checks default config."""
    c = _load_default_config()
    repo = c.get_repository_configuration("pypi")
    assert repo.name == "pypi"
    assert len(c.repository_names) == 1
    assert c.repository_names[0] == "pypi"
    assert c.report_configuration
    assert len(c.report_configuration.keys()) == 3
    assert set(c.report_configuration.keys()) == set(["basic", "safety", "spdx"])
    assert c.report_configuration["basic"] == ReportProviderConfiguration()
    assert c.report_configuration["spdx"] == ReportProviderConfiguration()
    assert c.report_configuration["safety"] == ReportProviderConfiguration()


def test_empty_config() -> None:
    """Checks config with no initial settings."""
    with pytest.raises(TypeError):
        Config()  # type: ignore


def test_bad_config_repeated_repos() -> None:
    """Checks config with repeated repository entries."""
    with pytest.raises(ValueError):
        Config(
            cache_dir="/var/cache",
            config_dir="/etc/valiant",
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


def test_multiple_repositories() -> None:
    """Ensure that the default repository is correct."""
    c = Config(
        cache_dir="/var/cache",
        config_dir="/etc/valiant",
        repository_configurations=[
            RepositoryConfiguration(name="test", base_url="https://www.example.com"),
            RepositoryConfiguration(
                name="test2", base_url="https://www.differentexample.com"
            ),
        ],
        default_repository="test2",
    )
    assert c.default_repository_name == "test2"
    assert c.default_repository_configuration.name == "test2"


def test_multiple_repositories_missing_default() -> None:
    """Ensure that the default repository is correct."""
    with pytest.raises(ValueError):
        Config(
            cache_dir="/var/cache",
            config_dir="/etc/valiant",
            repository_configurations=[
                RepositoryConfiguration(
                    name="test", base_url="https://www.example.com"
                ),
                RepositoryConfiguration(
                    name="test2", base_url="https://www.differentexample.com"
                ),
            ],
            default_repository="test9",
        )


def test_multiple_repositories_config_access() -> None:
    """Make sure the submitted repo configs can be correctly retrieved."""
    c = Config(
        cache_dir="/var/cache",
        config_dir="/etc/valiant",
        repository_configurations=[
            RepositoryConfiguration(name="test", base_url="https://www.example.com"),
            RepositoryConfiguration(
                name="test2", base_url="https://www.differentexample.com"
            ),
        ],
        default_repository="test2",
    )
    assert c.get_repository_configuration("test").name == "test"
    assert c.get_repository_configuration("test2").name == "test2"


def test_multiple_repositories_bad_config_access() -> None:
    """Ensure error when trying to access repo config that isn't there."""
    c = Config(
        cache_dir="/var/cache",
        config_dir="/etc/valiant",
        repository_configurations=[
            RepositoryConfiguration(name="test", base_url="https://www.example.com"),
            RepositoryConfiguration(
                name="test2", base_url="https://www.differentexample.com"
            ),
        ],
        default_repository="test2",
    )

    with pytest.raises(KeyError):
        c.get_repository_configuration("nurk")


def test_basic_config() -> None:
    """Basic config test."""
    c = Config(
        cache_dir="/var/cache",
        config_dir="/etc/valiant",
        repository_configurations=[PYPI_CONFIG],
    )
    assert c.cache_dir == Path("/var/cache")
    assert c.config_dir == Path("/etc/valiant")
    assert len(c.repository_names) == 1


def test_no_repo_config() -> None:
    """Expect failure."""
    with pytest.raises(ValueError):
        Config(
            cache_dir="/var/cache",
            config_dir="/etc/valiant",
            repository_configurations=[],
        )


def test_no_default_repo() -> None:
    """Expect failure."""
    with pytest.raises(ValueError):
        Config(
            cache_dir="/var/cache",
            config_dir="/etc/valiant",
            repository_configurations=[
                PYPI_CONFIG,
                RepositoryConfiguration(
                    name="test", base_url="https://www.example.com"
                ),
            ],
        )
