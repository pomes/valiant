"""Tests for the PyPi repo model."""

import json

from pathlib import Path
from typing import Dict

import py  # https://py.readthedocs.io/en/latest/index.html
import pytest

from valiant.repositories import ValidationError
from valiant.repositories.pypi import PyPiPackageMetadata

from .setup import ALL_PKG_FILES, DATAFILE_VALIDATION
from .test_data import BASIC_PKG, BASIC_PKG_2


def test_empty_package_data() -> None:
    """Ensures exception when constructor is passed an empty dict."""
    with pytest.raises(ValidationError):
        PyPiPackageMetadata({})


def test_json_load_basic() -> None:
    """Small baseline test."""
    pkg = PyPiPackageMetadata(BASIC_PKG)
    assert pkg.name == "Demo"
    assert pkg.description == "Basic description"
    assert pkg.summary == "A short summary."
    assert pkg.url_documentation == "http://docs.example.com"
    assert pkg.url_project == "http://project.example.com"
    assert pkg.url_issue_tracker == "http://bugs.example.com"


def test_json_load_basic2() -> None:
    """Small baseline test."""
    pkg = PyPiPackageMetadata(BASIC_PKG_2)
    assert pkg.name == "Demo 2"
    assert pkg.description == "Basic description"
    assert pkg.summary == "A short summary."
    assert pkg.url_documentation == "http://docs.example.com"
    assert pkg.url_project == "http://project.example.com"
    assert pkg.url_issue_tracker == "http://bugs.example.com"


def test_json_load_basic_to_dict() -> None:
    """Small baseline test of the string representation."""
    pkg = PyPiPackageMetadata(BASIC_PKG)
    val = pkg.to_dict()
    assert val["name"] == "Demo"
    assert val["version"] == "0"
    assert val["summary"] == "A short summary."


def test_json_load_basic_to_json() -> None:
    """Small baseline test of the string representation."""
    pkg = PyPiPackageMetadata(BASIC_PKG)
    json_val = pkg.to_json()
    val = json.loads(json_val)
    assert val["name"] == "Demo"
    assert val["version"] == "0"
    assert val["summary"] == "A short summary."


def test_json_load_basic_repr() -> None:
    """Small baseline test of the string representation."""
    pkg = PyPiPackageMetadata(BASIC_PKG)
    val = json.loads(str(pkg))
    assert val["name"] == "Demo"
    assert val["version"] == "0"
    assert val["summary"] == "A short summary."


@ALL_PKG_FILES
@pytest.mark.parametrize(
    ("input_file,expected"), DATAFILE_VALIDATION,
)
def test_json_load(datafiles: py.path, input_file: str, expected: Dict) -> None:
    """Validate loading against sample data from pypi.org."""
    source_data = Path(datafiles.join(input_file))
    with open(source_data, "r") as f:
        data = json.load(f)
    pkg = PyPiPackageMetadata(data)

    assert pkg.name == expected["name"]
    assert pkg.version == expected["version"]
    assert pkg.license == expected["license"]
    assert pkg.url_code == expected["url_code"]
    assert pkg.url_documentation == expected["url_documentation"]
    assert pkg.url_project == expected["url_project"]
    assert pkg.url_issue_tracker == expected["url_issue_tracker"]
    assert pkg.requires_python == expected["requires_python"]

    # This now gets messy - sorry
    # TODO: Tidy this up
    for k in expected["requires_dist"].keys():
        assert k in pkg.requires_dist

        reqs = [pkg._requirement_to_dict(item) for item in pkg.requires_dist[k]]
        expected_reqs = expected["requires_dist"][k]
        assert len(reqs) == len(expected["requires_dist"][k])

        # Iterate over the requirements in the source dependency
        for req in reqs:
            flag = False
            assert (
                k == req["name"]
            ), "All of the Requirements instances in the list must have the same name"

            # Inner loop - blech
            for ereq in expected_reqs:
                assert ereq["name"] == req["name"]
                print(f"Comparing {req} with {ereq}")
                if ereq == req:
                    flag = True
                    break

            assert flag, f"No match for requires_dist item: {ereq}."
