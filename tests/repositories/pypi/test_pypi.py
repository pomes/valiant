"""Basic tests of PyPi repo class."""

from valiant.repositories.pypi import PyPiRepository


def test_basic_config() -> None:
    """Checks for the repo config."""
    assert PyPiRepository().base_url == "https://pypi.org/pypi"
