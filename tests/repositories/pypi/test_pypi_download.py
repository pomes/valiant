"""Testing the PyPi repo show command."""
import pytest

from valiant.repositories.pypi import PyPiRepository

PYPI_CONFIG = PyPiRepository.get_pypi_config()


def test_basic() -> None:
    """Not implemented."""
    with pytest.raises(NotImplementedError):
        PyPiRepository(PYPI_CONFIG).download("flask", "1.1.1")
