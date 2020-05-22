"""Test configuration.

See: https://docs.pytest.org/en/latest/pythonpath.html

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
import os
import tempfile

from pathlib import Path
from typing import Generator

import pytest

from _pytest.config import Config

from . import MonkeyPatch


def pytest_configure(config: Config) -> None:  # noqa: D103
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")


@pytest.fixture
def valiant_version() -> str:
    """The expected app version."""
    return "0.2.2"  # noqa:DAR201


@pytest.fixture
def valiant_app_title() -> str:
    """The expected app title."""
    return "Valiant"  # noqa:DAR201


@pytest.fixture
def valiant_app_name() -> str:
    """The expected app name."""
    return "valiant"  # noqa:DAR201


@pytest.fixture
def valiant_license() -> str:
    """The expected app license."""
    return "MIT"  # noqa:DAR201


@pytest.fixture
def valiant_url() -> str:
    """The expected app url."""
    return "https://github.com/pomes/valiant"  # noqa:DAR201


# See:
# https://docs.pytest.org/en/latest/monkeypatch.html#global-patch-example-preventing-requests-from-remote-operations # noqa: B950
@pytest.fixture(autouse=True)
def no_requests(monkeypatch):  # noqa: ANN001, ANN201
    """Prevent requests lib from performing real requests.

    Remove requests.sessions.Session.request for all tests.
    """
    # I just can't seem to get the tests to run with the line below.
    # Any thoughts would be really appreciated

    # monkeypatch.delattr("requests.sessions.Session.request")

    monkeypatch.setattr("requests_cache.install_cache", lambda *a, **kw: None)


@pytest.fixture(autouse=True)
def override_appdirs(monkeypatch: MonkeyPatch, tmp_path: Path):  # noqa: ANN001, ANN201
    """Have appdirs use test dirs.

    See: https://pypi.org/project/appdirs/
    """
    import appdirs

    monkeypatch.setattr(
        appdirs,
        "user_data_dir",
        lambda appname, appauthor, version, roaming: tmp_path / "user_data_dir",
    )

    monkeypatch.setattr(
        appdirs,
        "user_config_dir",
        lambda appname, appauthor, version, roaming: tmp_path / "user_config_dir",
    )

    monkeypatch.setattr(
        appdirs,
        "user_cache_dir",
        lambda appname, appauthor, version: tmp_path / "user_cache_dir",
    )

    monkeypatch.setattr(
        appdirs,
        "user_log_dir",
        lambda appname, appauthor, version: tmp_path / "user_log_dir",
    )

    monkeypatch.setattr(
        appdirs,
        "site_data_dir",
        lambda appname, appauthor, version, multipath: tmp_path / "site_data_dir",
    )

    monkeypatch.setattr(
        appdirs,
        "site_config_dir",
        lambda appname, appauthor, version, multipath: tmp_path / "site_config_dir",
    )


@pytest.fixture(scope="function")
def clean_up_tmp_folder():  # noqa:ANN201
    """Provides a tidyup for tests that use /tmp/valiant_test.

    This is primarily used for tests involving config files so
    that a known path can be used.

    Yields:
        Nothing
    """
    from pathlib import Path  # noqa:DAR301
    import shutil

    p = Path("/tmp/valiant_test")
    yield
    if p.exists():
        shutil.rmtree(p)


@pytest.fixture
def cleandir() -> Generator:
    """Sets the CWD to a temp dir.

    #noqa: DAR301

    See: https://docs.pytest.org/en/latest/fixture.html \
            #using-fixtures-from-classes-modules-or-projects
    """
    import shutil

    old_cwd = os.getcwd()
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    yield
    os.chdir(old_cwd)
    shutil.rmtree(newpath)
