"""Test loading data files.

See: https://docs.pytest.org/en/latest/monkeypatch.html#monkeypatching-returned-objects-building-mock-classes # noqa: B950
"""

import datetime

from typing import Any, Dict

import pytest
import requests

from valiant.plugins.reports.spdx import SpdxLicenses


MonkeyPatch = Any

BASIC_PAYLOAD = {
    "licenseListVersion": "test-01",
    "releaseDate": "1901-01-01",
    "licenses": [
        {
            "reference": "./0BSD.html",
            "isDeprecatedLicenseId": False,
            "detailsUrl": "http://spdx.org/licenses/0BSD.json",
            "referenceNumber": "231",
            "name": "BSD Zero Clause License",
            "licenseId": "0BSD",
            "seeAlso": ["http://landley.net/toybox/license.html"],
            "isOsiApproved": True,
        }
    ],
}


class MockResponse:
    """Basic mock for requests.get response."""

    def __init__(self, status_code: int, json_data: Any):  # noqa: D107
        self.status_code = status_code
        self.json_data = json_data

    def json(self) -> Any:  # noqa: D102
        return self.json_data


def test_loader(monkeypatch: MonkeyPatch) -> None:
    """Load a basic dataset."""
    licenses = SpdxLicenses.loader(data=BASIC_PAYLOAD)

    assert licenses.version == "test-01"
    assert licenses.release_date == datetime.date(1901, 1, 1)


def test_url_loader_basic(monkeypatch: MonkeyPatch) -> None:
    """Load a basic dataset from a URL."""

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=200, json_data=BASIC_PAYLOAD,)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    licenses = SpdxLicenses.url_loader(url="http://www.example.com")

    assert licenses.version == "test-01"
    assert licenses.release_date == datetime.date(1901, 1, 1)


class MockResponseFailedRequest:
    """Basic mock for failed HTTP requests."""

    def __init__(self):  # noqa: DA
        self.status_code = 404


def test_url_loader_failed_request(monkeypatch: MonkeyPatch) -> None:
    """Test a failed url load."""

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=404, json_data=None)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValueError):
        _ = SpdxLicenses.url_loader(url="http://www.example.com")


def test_url_loader_missing_data(monkeypatch: MonkeyPatch) -> None:
    """Test an empty JSON payload."""

    def mock_get(*args, **kwargs):  # noqa: ANN
        return MockResponse(status_code=200, json_data={})

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValueError):
        _ = SpdxLicenses.url_loader(url="http://www.example.com")


def test_url_loader_missing_data_version(monkeypatch: MonkeyPatch) -> None:
    """Test a JSON payload with no version."""

    def mock_get(*args, **kwargs):  # noqa: ANN
        payload = dict(BASIC_PAYLOAD)
        payload["version"] = None
        return MockResponse(status_code=200, json_data=payload)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValueError):
        _ = SpdxLicenses.url_loader(url="http://www.example.com")


def test_url_loader_missing_data_release_date(monkeypatch: MonkeyPatch) -> None:
    """Test a JSON payload with no version."""

    def mock_get(*args, **kwargs):  # noqa: ANN
        payload = dict(BASIC_PAYLOAD)
        payload["releaseDate"] = None
        return MockResponse(status_code=200, json_data=payload)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValueError):
        _ = SpdxLicenses.url_loader(url="http://www.example.com")


def test_url_loader_missing_data_licenses(monkeypatch: MonkeyPatch) -> None:
    """Test a JSON payload with no licenses.

    The license list is allowed to be empty. It's pointless but shouldn't
    cause an exception.
    """

    def mock_get(*args, **kwargs):  # noqa: ANN
        payload = dict(BASIC_PAYLOAD)
        payload["licenses"] = []
        return MockResponse(status_code=200, json_data=payload)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    licenses = SpdxLicenses.url_loader(url="http://www.example.com")
    assert isinstance(licenses.licenses, Dict)
    assert len(licenses.licenses.keys()) == 0


def test_url_loader_missing_data_single_license(monkeypatch: MonkeyPatch) -> None:
    """Test a JSON payload with missing license data."""

    def mock_get(*args, **kwargs):  # noqa: ANN
        payload = dict(BASIC_PAYLOAD)
        # Note: No name for the license
        payload["licenses"] = [
            {
                "reference": "./0BSD.html",
                "isDeprecatedLicenseId": False,
                "detailsUrl": "http://spdx.org/licenses/0BSD.json",
                "referenceNumber": "231",
                "licenseId": "0BSD",
                "seeAlso": ["http://landley.net/toybox/license.html"],
                "isOsiApproved": True,
            }
        ]
        return MockResponse(status_code=200, json_data=payload)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValueError):
        _ = SpdxLicenses.url_loader(url="http://www.example.com")


def test_url_loader_missing_data_single_license_noid(monkeypatch: MonkeyPatch) -> None:
    """Test a JSON payload with missing license data - no licenseId."""

    def mock_get(*args, **kwargs):  # noqa: ANN
        payload = dict(BASIC_PAYLOAD)
        # Note: No name for the license
        payload["licenses"] = [
            {
                "reference": "./0BSD.html",
                "isDeprecatedLicenseId": False,
                "detailsUrl": "http://spdx.org/licenses/0BSD.json",
                "referenceNumber": "231",
                "name": "BSD Zero Clause License",
                "seeAlso": ["http://landley.net/toybox/license.html"],
                "isOsiApproved": True,
            }
        ]
        return MockResponse(status_code=200, json_data=payload)

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValueError):
        _ = SpdxLicenses.url_loader(url="http://www.example.com")
