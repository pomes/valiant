"""Make sure abstract classes don't do anything.

Copyright (c) 2020 The Valiant Authors

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import pytest

from valiant.repositories import BaseRepository, RepositoryConfiguration


def test_base_repository() -> None:
    """Ensure that instantiating the class raises TypeError."""
    with pytest.raises(TypeError):
        BaseRepository()  # type: ignore


def test_base_repository_supported_repo_types() -> None:
    """Ensure that the base class supports nothing."""
    assert BaseRepository.list_supported_repository_types() == []


def test_repo_config_basic() -> None:
    """Test using the basic (pypi) repo."""
    repo = RepositoryConfiguration(name="pypi", base_url="https://pypi.org/pypi")
    assert repo.get_access_url() == "https://pypi.org/pypi"
    assert repo.name == "pypi"
    assert repo.repository_type == "unknown"

    d = repo.to_dict()
    assert d["name"] == "pypi"


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
