"""PyPi Repo tests.

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
import os

from typing import Dict

import py  # https://py.readthedocs.io/en/latest/index.html
import pytest

from ... import MockResponse, MonkeyPatch  # noqa: F401
from .validation import DATAFILE_VALIDATION  # noqa: F401


_dir = os.path.dirname(os.path.realpath(__file__))

TEST_FILE_DIR = py.path.local(_dir) / "test-data"

# Setup the datafiles: https://pypi.org/project/pytest-datafiles/
FIXTURE_DIR = py.path.local(_dir) / "package-data"

_json_files = [
    os.path.join(FIXTURE_DIR / j) for j in os.listdir(FIXTURE_DIR) if j[-4:] == "json"
]

ALL_PKG_FILES = pytest.mark.datafiles(*_json_files)
# End setup


def load_test_json_data(path: py.path, filename: str) -> Dict:  # noqa: ANN
    with open(path / filename, "r") as f:
        package_data = json.load(f)

    return package_data
