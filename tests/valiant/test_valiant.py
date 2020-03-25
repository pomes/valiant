"""Basic test suite."""
from pathlib import Path

import pytest

from valiant import Factory, Valiant
from valiant.config import Config
from valiant.repositories.pypi import PyPiRepository


def test_application_details() -> None:
    """Validate the general app info."""
    v = Factory().create_valiant()
    assert v.application_version == "0.1.0"
    assert v.application_name == "valiant"
    assert v.application_title == "Valiant"
    assert v.application_vendor == "Pomes"
    assert v.application_tagline == "Dependency Investigations Unit"
    assert v.application_description == "Valiant helps you investigate dependencies"
    assert v.application_licence == "MIT"
    assert v.application_homepage == "https://github.com/pomes/valiant"
    assert v.application_copyright_year == 2020
    assert v.application_copyright_holder == "Duncan Dickinson"


def test_config_empty() -> None:
    """Testing valiant configuration."""
    with pytest.raises(TypeError):
        Valiant()


def test_config_missing_repo_config() -> None:
    """Testing valiant configuration custom settings."""
    with pytest.raises(ValueError):
        Config(
            cache_dir="/var/cache",
            config_dir="/etc/valiant",
            repository_configurations=[],
        )


def test_config_default() -> None:
    """Tests the factory defaults."""
    v = Factory().create_valiant()
    assert v.cache_dir is not None
    assert v.config_dir is not None


def test_config_custom() -> None:
    """Testing valiant configuration custom settings."""
    c = Config(
        cache_dir="/var/cache",
        config_dir="/etc/valiant",
        repository_configurations=[PyPiRepository.get_pypi_config()],
    )
    v = Factory().create_valiant(c)
    assert v.cache_dir == Path("/var/cache")
    assert v.config_dir == Path("/etc/valiant")


def test_reports_no_config() -> None:
    """Fail if no report configuration has been provided."""
    c = Config(
        cache_dir="/var/cache",
        config_dir="/etc/valiant",
        repository_configurations=[PyPiRepository.get_pypi_config()],
    )
    v = Factory().create_valiant(c)
    with pytest.raises(ValueError):
        v.get_package_reports()
