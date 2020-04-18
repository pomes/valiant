"""Tests for loading the files in package-data/.

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
import json
from pathlib import Path

import py
import requests

from valiant.repositories import RepositoryConfiguration
from valiant.repositories.pypi import PyPiRepository

from . import MockResponse

from . import ALL_PKG_FILES, MonkeyPatch


@ALL_PKG_FILES
def test_data_load(
    monkeypatch: MonkeyPatch, datafiles: py.path, pypi_config: RepositoryConfiguration
) -> None:
    """Validate loading against sample data from pypi.org."""
    for data_file in datafiles.listdir():

        with open(data_file, "r") as f:
            data = json.load(f)

        def mock_get(*args, **kwargs):  # noqa: ANN
            return MockResponse(status_code=200, json_data=data)

        # apply the monkeypatch for requests.get to mock_get
        monkeypatch.setattr(requests, "get", mock_get)

        p = Path(data_file.basename)
        pname, _, pversion = p.stem.rpartition("-")

        pkg = PyPiRepository(pypi_config).show(pname, pversion)

        assert pkg.name.lower() == pname.lower()
        assert pkg.version == pversion
