"""Tests for the PyPi repo model."""

import json

from pathlib import Path
from typing import Dict

import py  # https://py.readthedocs.io/en/latest/index.html
import pytest

from valiant.repositories import RepositoryConfiguration, ValidationError
from valiant.repositories.pypi import PyPiPackageMetadata

from . import ALL_PKG_FILES, DATAFILE_VALIDATION, TEST_FILE_DIR, load_test_json_data


def test_empty_package_data() -> None:
    """Ensures exception when constructor is passed an empty dict."""
    with pytest.raises(ValidationError):
        PyPiPackageMetadata("", {})


@pytest.mark.datafiles(TEST_FILE_DIR / "basic_package.json")
def test_json_load_basic(
    datafiles: py.path, pypi_config: RepositoryConfiguration
) -> None:
    """Small baseline test."""
    pkg = PyPiPackageMetadata(
        pypi_config.base_url, load_test_json_data(datafiles, "basic_package.json")
    )
    assert pkg.name == "Demo"
    assert pkg.description == "Basic description"
    assert pkg.summary == "A short summary."
    assert pkg.url_documentation == "http://docs.example.com"
    assert pkg.url_project == "http://project.example.com"
    assert pkg.url_issue_tracker == "http://bugs.example.com"
    assert pkg.repository_url == pypi_config.base_url


@pytest.mark.datafiles(TEST_FILE_DIR / "basic_package_2.json")
def test_json_load_basic2(
    datafiles: py.path, pypi_config: RepositoryConfiguration
) -> None:
    """Small baseline test."""
    pkg = PyPiPackageMetadata(
        pypi_config.base_url, load_test_json_data(datafiles, "basic_package_2.json")
    )
    assert pkg.name == "Demo 2"
    assert pkg.description == "Basic description"
    assert pkg.summary == "A short summary."
    assert pkg.url_documentation == "http://docs.example.com"
    assert pkg.url_project == "http://project.example.com"
    assert pkg.url_issue_tracker == "http://bugs.example.com"


@pytest.mark.datafiles(TEST_FILE_DIR / "basic_package_3.json")
def test_json_load_basic3(
    datafiles: py.path, pypi_config: RepositoryConfiguration
) -> None:
    """Small baseline test."""
    pkg = PyPiPackageMetadata(
        pypi_config.base_url, load_test_json_data(datafiles, "basic_package_3.json")
    )
    assert pkg.name == "Demo 2"
    assert pkg.description == "Basic description"
    assert pkg.summary == "A short summary."
    assert pkg.url_documentation == "http://docs.example.com"
    assert pkg.url_project == "http://project.example.com"
    assert pkg.url_issue_tracker == "http://bugs.example.com"


@pytest.mark.datafiles(TEST_FILE_DIR / "basic_package.json")
def test_json_load_basic_to_dict(
    datafiles: py.path, pypi_config: RepositoryConfiguration
) -> None:
    """Small baseline test of the string representation."""
    pkg = PyPiPackageMetadata(
        pypi_config.base_url, load_test_json_data(datafiles, "basic_package.json")
    )
    val = pkg.to_dict()
    assert val["name"] == "Demo"
    assert val["version"] == "0"
    assert val["summary"] == "A short summary."


@pytest.mark.datafiles(TEST_FILE_DIR / "basic_package.json")
def test_json_load_basic_to_json(
    datafiles: py.path, pypi_config: RepositoryConfiguration
) -> None:
    """Small baseline test of the string representation."""
    pkg = PyPiPackageMetadata(
        pypi_config.base_url, load_test_json_data(datafiles, "basic_package.json")
    )
    json_val = pkg.to_json()
    val = json.loads(json_val)
    assert val["name"] == "Demo"
    assert val["version"] == "0"
    assert val["summary"] == "A short summary."


@pytest.mark.datafiles(TEST_FILE_DIR / "basic_package.json")
def test_json_load_basic_repr(
    datafiles: py.path, pypi_config: RepositoryConfiguration
) -> None:
    """Small baseline test of the string representation."""
    pkg = PyPiPackageMetadata(
        pypi_config.base_url, load_test_json_data(datafiles, "basic_package.json")
    )
    val = json.loads(str(pkg))
    assert val["name"] == "Demo"
    assert val["version"] == "0"
    assert val["summary"] == "A short summary."


@ALL_PKG_FILES
@pytest.mark.parametrize(
    ("input_file,expected"), DATAFILE_VALIDATION,
)
def test_json_load(
    input_file: str,
    expected: Dict,
    datafiles: py.path,
    pypi_config: RepositoryConfiguration,
) -> None:
    """Validate loading against sample data from pypi.org.

    This is different to test_data_load.py as this test is more than
    just a basic load. The DATAFILE_VALIDATION consttruct lays out
    a set of attributes to test against for the various inputs.
    """
    source_data = Path(datafiles.join(input_file))
    with open(source_data, "r") as f:
        data = json.load(f)
    pkg = PyPiPackageMetadata(pypi_config.base_url, data)

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
