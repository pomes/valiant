"""PyPi Repo tests."""
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
