"""Basic tests of PyPi repo class.

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
