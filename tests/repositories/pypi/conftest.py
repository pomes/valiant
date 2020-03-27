"""Shared test assets."""
import pytest

from valiant.repositories import RepositoryConfiguration
from valiant.repositories.pypi import PyPiRepository


@pytest.fixture
def pypi_config() -> RepositoryConfiguration:
    """Returns the default PyPi config."""
    return PyPiRepository.get_pypi_config()  # noqa:DAR201
