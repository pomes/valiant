"""Testing the PyPi repo show command."""
import json

from pathlib import Path
from typing import Dict

import py  # https://py.readthedocs.io/en/latest/index.html
import pytest
import requests

from valiant.repositories import PackageNotFoundException
from valiant.repositories.pypi import PyPiRepository

from .setup import ALL_PKG_FILES, DATAFILE_VALIDATION, MockResponse, MonkeyPatch
from .test_data import BASIC_PKG

PYPI_CONFIG = PyPiRepository.get_pypi_config()


def test_basic(monkeypatch: MonkeyPatch) -> None:
    """Test a basic package manifest."""

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=200, json_data=BASIC_PKG)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    pkg = PyPiRepository(PYPI_CONFIG).show("flask", "-1.1.1")
    assert pkg.name == "Demo"


def test_fail(monkeypatch: MonkeyPatch) -> None:
    """Test a failed attempt to download a package manifest."""

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=404, json_data={})

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(PackageNotFoundException):
        PyPiRepository(PYPI_CONFIG).show("FAKE", "-3.14")


def test_empty_json(monkeypatch: MonkeyPatch) -> None:
    """Test handling of an HTTP success that returns an empty manifest."""

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=200, json_data=None)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(PackageNotFoundException):
        PyPiRepository(PYPI_CONFIG).show("FAKE", "-3.14")


@ALL_PKG_FILES
@pytest.mark.parametrize(
    ("input_file,expected"), DATAFILE_VALIDATION,
)
def test_json_load(
    monkeypatch: MonkeyPatch, datafiles: py.path, input_file: str, expected: Dict
) -> None:
    """Validate loading against sample data from pypi.org."""
    source_data = Path(datafiles.join(input_file))
    with open(source_data, "r") as f:
        data = json.load(f)

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=200, json_data=data)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    pkg = PyPiRepository(PYPI_CONFIG).show("X", "-1")

    assert pkg.name == expected["name"]
    assert pkg.version == expected["version"]
    assert pkg.license == expected["license"]
