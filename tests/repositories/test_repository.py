"""Make sure abstract classes don't do anything."""

import pytest

from valiant.repositories import BaseRepository, RepositoryConfiguration


def test_base_repository() -> None:
    """Ensure that instantiating the class raises TypeError."""
    with pytest.raises(TypeError):
        BaseRepository()  # type: ignore


def test_repo_config_basic() -> None:
    """Test using the basic (pypi) repo."""
    repo = RepositoryConfiguration(name="pypi", base_url="https://pypi.org/pypi")
    assert repo.get_access_url() == "https://pypi.org/pypi"
    assert repo.name == "pypi"
    assert repo.repository_type == "unknown"


def test_repo_config_basic_port() -> None:
    """Test using the basic (pypi) repo."""
    repo = RepositoryConfiguration(name="pypi", base_url="https://pypi.org:443/pypi")
    assert repo.get_access_url() == "https://pypi.org:443/pypi"
    assert repo.name == "pypi"


def test_repo_config_userpass() -> None:
    """Test using repo with username/password."""
    password = "pa55word"  # noqa: S106
    repo = RepositoryConfiguration(
        name="pypi",
        base_url="https://private.repo.org/pypi",
        username="fred",
        password=password,
    )
    assert repo.get_access_url() == f"https://fred:{password}@private.repo.org/pypi"


def test_repo_config_userpass_port() -> None:
    """Test using repo with username/password."""
    password = "pa55word"  # noqa: S106
    repo = RepositoryConfiguration(
        name="pypi",
        base_url="https://private.repo.org:8080/pypi",
        username="fred",
        password=password,
    )
    assert (
        repo.get_access_url() == f"https://fred:{password}@private.repo.org:8080/pypi"
    )


def test_repo_config_token() -> None:
    """Test using repo with token."""
    token = "clksd88sadh4HhJ"  # noqa: S106
    repo = RepositoryConfiguration(
        name="pypi", base_url="https://private.repo.org/pypi", token=token,
    )
    assert repo.get_access_url() == f"https://{token}@private.repo.org/pypi"


def test_repo_config_token_port() -> None:
    """Test using repo with token."""
    token = "clksd88sadh4HhJ"  # noqa: S106
    repo = RepositoryConfiguration(
        name="pypi",
        base_url="https://private.repo.org:8080/pypi",
        username="fred",
        token=token,
    )
    assert repo.get_access_url() == f"https://{token}@private.repo.org:8080/pypi"
