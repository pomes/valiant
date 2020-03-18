"""Testing the PyPi repo show command."""
import pytest

from valiant.repositories.pypi import PyPiRepository


def test_basic() -> None:
    """Not implemented."""
    with pytest.raises(NotImplementedError):
        PyPiRepository().download("flask", "1.1.1")
