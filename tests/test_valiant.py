"""Basic test suite."""
from valiant import __version__


def test_version():
    """Validate the version"""
    assert __version__ == "0.1.0"
