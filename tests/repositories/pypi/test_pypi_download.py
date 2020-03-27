"""Testing the PyPi repo show command."""
import pytest

from valiant.repositories import RepositoryConfiguration
from valiant.repositories.pypi import PyPiRepository


def test_basic(pypi_config: RepositoryConfiguration) -> None:
    """Not implemented."""
    with pytest.raises(NotImplementedError):
        PyPiRepository(pypi_config).download("flask", "1.1.1")
