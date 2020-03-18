"""Provides the datafile config."""
import os

from typing import Any

import py  # https://py.readthedocs.io/en/latest/index.html
import pytest


_dir = os.path.dirname(os.path.realpath(__file__))
FIXTURE_DIR = py.path.local(_dir) / "data"

ALL_PKG_FILES = pytest.mark.datafiles(
    FIXTURE_DIR / "flask-1.1.1.json",
    FIXTURE_DIR / "gpiozero-1.5.1.json",
    FIXTURE_DIR / "opencv-python-4.2.0.32.json",
    FIXTURE_DIR / "tensorflow-2.1.0.json",
)

DATAFILE_VALIDATION = [
    (
        "flask-1.1.1.json",
        {
            "name": "Flask",
            "version": "1.1.1",
            "license": "BSD-3-Clause",
            "url_code": "https://github.com/pallets/flask",
            "url_documentation": "https://flask.palletsprojects.com/",
            "url_project": "https://palletsprojects.com/p/flask/",
            "url_issue_tracker": "https://github.com/pallets/flask/issues",
            "requires_python": [
                ">=2.7",
                "!=3.0.*",
                "!=3.1.*",
                "!=3.2.*",
                "!=3.3.*",
                "!=3.4.*",
            ],
            "requires_dist": {
                "Werkzeug": [
                    {
                        "name": "Werkzeug",
                        "url": None,
                        "specifiers": [
                            {"version": "0.15", "operator": ">=", "prereleases": False}
                        ],
                        "extras": [],
                        "marker": None,
                    }
                ],
                "pallets-sphinx-themes": [
                    {
                        "name": "pallets-sphinx-themes",
                        "url": None,
                        "specifiers": [],
                        "extras": [],
                        "marker": 'extra == "dev"',
                    },
                    {
                        "name": "pallets-sphinx-themes",
                        "url": None,
                        "specifiers": [],
                        "extras": [],
                        "marker": 'extra == "docs"',
                    },
                ],
            },
        },
    )
]

MonkeyPatch = Any


class MockResponse:
    """Basic mock for requests.get response."""

    def __init__(self, status_code: int, json_data: Any):  # noqa: D107
        self.status_code = status_code
        self.json_data = json_data

    def json(self) -> Any:  # noqa: D102
        return self.json_data
