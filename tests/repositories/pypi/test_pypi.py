"""Basic tests of PyPi repo class."""

from valiant.repositories.pypi import PyPiRepository

PYPI_CONFIG = PyPiRepository.get_pypi_config()


def test_basic_config() -> None:
    """Checks for the repo config."""
    assert (
        PyPiRepository(PYPI_CONFIG).repository_configuration.get_access_url()
        == "https://pypi.org/pypi"
    )


def test_pypi_config() -> None:
    """Checks the helper config for PyPi."""
    config = PYPI_CONFIG
    assert config.name == "pypi"
    assert config.get_access_url() == "https://pypi.org/pypi"
    assert config.repository_type == "warehouse"
