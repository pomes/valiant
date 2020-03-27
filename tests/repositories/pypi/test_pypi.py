"""Basic tests of PyPi repo class."""
import pytest

from valiant.repositories import RepositoryConfiguration
from valiant.repositories.pypi import PyPiRepository


def test_basic_config(pypi_config: RepositoryConfiguration) -> None:
    """Checks for the repo config."""
    assert (
        PyPiRepository(pypi_config).repository_configuration.get_access_url()
        == "https://pypi.org/pypi"
    )


def test_pypi_config(pypi_config: RepositoryConfiguration) -> None:
    """Checks the helper config for PyPi."""
    config = pypi_config
    assert config.name == "pypi"
    assert config.get_access_url() == "https://pypi.org/pypi"
    assert config.repository_type == "warehouse"


def test_pypi_repo_config(pypi_config: RepositoryConfiguration) -> None:
    """Checks the repository config comes through correctly."""
    repo = PyPiRepository(pypi_config)
    assert repo.repository_type == "warehouse"
    assert PyPiRepository.list_supported_repository_types() == ["warehouse", "pypi"]


def test_repository_no_config(pypi_config: RepositoryConfiguration) -> None:
    """Ensure that instantiating without config raises an error."""
    with pytest.raises(TypeError):
        PyPiRepository()  # type: ignore


def test_repository_unsupported_config(pypi_config: RepositoryConfiguration) -> None:
    """Ensure that config with an unsupported type is booted ."""
    with pytest.raises(ValueError):
        PyPiRepository(
            RepositoryConfiguration(
                name="broken", base_url="http://myrepo.com", repository_type="maven"
            )
        )
