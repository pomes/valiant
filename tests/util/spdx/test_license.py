"""SPDX license tests.

For details regarding pytest-datafiles see: https://pypi.org/project/pytest-datafiles/
"""
import json
import os

from datetime import date
from typing import Dict

import py  # https://py.readthedocs.io/en/latest/index.html
import pytest

from valiant.util.spdx import SpdxLicense, SpdxLicenses


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "data", "license-files"
)


@pytest.fixture
def licenses() -> SpdxLicenses:
    """Load the SPDX licenses from the included pickle file.

    Returns:
        The licences
    """
    licenses = SpdxLicenses.builtin_loader()
    return licenses


def test_builtin_loader_release_attributes(licenses: SpdxLicenses,) -> None:
    """Tests that the SPDX license data can be unpickled."""
    assert licenses.release_date == date(2020, 3, 11)
    assert licenses.version == "3.8-22-gbcb6222"
    assert isinstance(licenses.licenses, Dict)


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "licenses.json"),)
def test_json_load(datafiles: py.path) -> None:
    """Test loading SPDX Json data files."""
    for infile in datafiles.listdir():
        with open(infile, "r") as f:
            data = json.load(f)

        lic = SpdxLicenses.loader(data)
        assert lic.version
        assert lic.release_date
        assert isinstance(lic.release_date, date)

        for k, v in lic.licenses.items():
            assert isinstance(v, SpdxLicense)
            assert k == v.id

        mit = lic.get_license("MIT")

        assert mit is not None

        assert mit.id == "MIT"
        assert mit.is_osi_approved
        assert mit.is_fsf_libre
        assert mit.name == "MIT License"
        assert mit.details_url == "http://spdx.org/licenses/MIT.json"
