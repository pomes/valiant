"""Tests for loading the files in package-data/."""
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
