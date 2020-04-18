"""Test setups.

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
from pathlib import Path

import pytest

from appdirs import AppDirs

from valiant.config import ConfigBuilder
from valiant.repositories import RepositoryConfiguration


@pytest.fixture
def appdirs() -> AppDirs:
    """Provide a configured AppDirs instance."""
    return AppDirs("valiant", "test", version="1.0")  # noqa:DAR201


@pytest.fixture
def appdirs_created(appdirs: AppDirs) -> AppDirs:
    """Creates directories for all AppDirs and returns the AppDirs instance."""
    appdirs.user_data_dir.mkdir(parents=True, exist_ok=True)  # noqa:DAR201
    appdirs.user_config_dir.mkdir(parents=True, exist_ok=True)
    appdirs.user_cache_dir.mkdir(parents=True, exist_ok=True)
    appdirs.user_log_dir.mkdir(parents=True, exist_ok=True)

    appdirs.site_data_dir.mkdir(parents=True, exist_ok=True)
    appdirs.site_config_dir.mkdir(parents=True, exist_ok=True)

    return appdirs


@pytest.fixture(scope="function")
def copy_test_files():  # noqa:ANN201
    """Helper to copy files to a specific location."""
    import os  # noqa:DAR301
    import shutil

    base = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data",)
    files = ["logging.conf"]
    test_dir = Path("/tmp/valiant_test_data")
    test_dir.mkdir(exist_ok=True)

    for f in files:
        p = Path(base, f)
        shutil.copyfile(p, test_dir / f)

    yield
    # Tidy up at completion
    # See: https://docs.pytest.org/en/latest/fixture.html \
    #           #fixture-finalization-executing-teardown-code
    shutil.rmtree(test_dir)


@pytest.fixture(scope="function")
def config_default_builder(tmp_path: Path) -> ConfigBuilder:
    """Create a builder using only the base config ready for test runs.

    Returns:
        ConfigBuilder instance.
    """
    from valiant.config.util import create_valiant_builder

    builder = create_valiant_builder(
        include_pyproject=False, include_user_config=False, include_site_config=False
    )
    return builder


@pytest.fixture(scope="function")
def config_builder(tmp_path: Path) -> ConfigBuilder:
    """Create a builder using only the base config ready for test runs.

    Returns:
        ConfigBuilder instance.
    """
    from valiant.config.util import create_valiant_builder

    builder = create_valiant_builder()
    return builder


@pytest.fixture
def pypi_repo() -> RepositoryConfiguration:
    """Gets the default PyPi repo config.

    Returns:
        A repo config for Pypi.
    """
    from valiant.repositories.pypi import PyPiRepository

    return PyPiRepository.get_pypi_config()  # noqa:DAR201
