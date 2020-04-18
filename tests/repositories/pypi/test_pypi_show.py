"""Testing the PyPi repo show command.

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

from typing import Dict

import py  # https://py.readthedocs.io/en/latest/index.html
import pytest
import requests

from valiant.package import Classifier
from valiant.repositories import (
    PackageNotFoundException,
    RepositoryConfiguration,
    ValidationError,
)
from valiant.repositories.pypi import PyPiRepository

from . import (
    ALL_PKG_FILES,
    DATAFILE_VALIDATION,
    TEST_FILE_DIR,
    MockResponse,
    MonkeyPatch,
)


@pytest.mark.datafiles(TEST_FILE_DIR / "basic_package.json")
def test_basic(
    monkeypatch: MonkeyPatch, pypi_config: RepositoryConfiguration, datafiles: py.path
) -> None:
    """Test a basic package manifest."""
    with open(datafiles / "basic_package.json", "r") as f:
        package_data = json.load(f)

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=200, json_data=package_data)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    pkg = PyPiRepository(pypi_config).show("flask", "-1.1.1")
    assert pkg.name == "Demo"


@pytest.mark.datafiles(TEST_FILE_DIR / "basic_package.json")
def test_basic_classifiers(
    monkeypatch: MonkeyPatch, pypi_config: RepositoryConfiguration, datafiles: py.path
) -> None:
    """Test the classifiers in the basic package manifest."""
    with open(datafiles / "basic_package.json", "r") as f:
        package_data = json.load(f)

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=200, json_data=package_data)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    pkg = PyPiRepository(pypi_config).show("flask", "-1.1.1")
    test_classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
    ]

    assert len(pkg.classifiers) == 2
    assert pkg.classifiers == test_classifiers

    assert len(pkg.classifiers_parsed) == 2

    classifiers = [Classifier.parse(c) for c in test_classifiers]

    for c in classifiers:
        assert c in pkg.classifiers_parsed


def test_fail(monkeypatch: MonkeyPatch, pypi_config: RepositoryConfiguration) -> None:
    """Test a failed attempt to download a package manifest."""

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=404, json_data={})

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(PackageNotFoundException):
        PyPiRepository(pypi_config).show("FAKE", "-3.14")


def test_empty_json(
    monkeypatch: MonkeyPatch, pypi_config: RepositoryConfiguration
) -> None:
    """Test handling of an HTTP success that returns an empty manifest."""

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=200, json_data=None)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(PackageNotFoundException):
        PyPiRepository(pypi_config).show("FAKE", "-3.14")


@pytest.mark.datafiles(TEST_FILE_DIR / "broken_package.json")
def test_bad_package_fails(
    monkeypatch: MonkeyPatch, pypi_config: RepositoryConfiguration, datafiles: py.path
) -> None:
    """Ensures a package missing the name will fail."""
    with open(datafiles / "broken_package.json", "r") as f:
        package_data = json.load(f)

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=200, json_data=package_data)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValidationError):
        PyPiRepository(pypi_config).show("FAKE", "-3.14")


@ALL_PKG_FILES
@pytest.mark.parametrize(
    ("input_file,expected"), DATAFILE_VALIDATION,
)
def test_json_load(
    monkeypatch: MonkeyPatch,
    pypi_config: RepositoryConfiguration,
    datafiles: py.path,
    input_file: str,
    expected: Dict,
) -> None:
    """Validate loading against sample data from pypi.org."""
    with open(datafiles / input_file, "r") as f:
        data = json.load(f)

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=200, json_data=data)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    pkg = PyPiRepository(pypi_config).show("X", "-1")

    assert pkg.name == expected["name"]
    assert pkg.version == expected["version"]
    assert pkg.license == expected["license"]
    assert pkg.classifiers_parsed
