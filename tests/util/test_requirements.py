"""Test for valiant.util.requirements.

Copyright 2021 The Valiant Authors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
from pathlib import Path

import py  # https://py.readthedocs.io/en/latest/index.html
import pytest

from valiant.util import (
    RequirementEntry,
    parse_requirements_file,
    parse_requirements_entry,
)

_dir = os.path.dirname(os.path.realpath(__file__))

REQ_DIR = py.path.local(_dir) / "req_data"

_req_files = [os.path.join(REQ_DIR / j) for j in os.listdir(REQ_DIR) if j[-3:] == "txt"]

ALL_REQ_FILES = pytest.mark.datafiles(*_req_files)

tests = [
    (
        "packaging",
        RequirementEntry(
            package="packaging",
            versions=[],
            extras=[],
            environment_markers=None,
            hashes=None,
        ),
    ),
    (
        "packaging==20.7",
        RequirementEntry(
            package="packaging",
            versions=[("==", "20.7")],
            extras=[],
            environment_markers=None,
            hashes=None,
        ),
    ),
    (
        "packaging== 20.7",
        RequirementEntry(
            package="packaging",
            versions=[("==", "20.7")],
            extras=[],
            environment_markers=None,
            hashes=None,
        ),
    ),
    (
        "packaging == 20.7",
        RequirementEntry(
            package="packaging",
            versions=[("==", "20.7")],
            extras=[],
            environment_markers=None,
            hashes=None,
        ),
    ),
    (
        "packaging ==20.7",
        RequirementEntry(
            package="packaging",
            versions=[("==", "20.7")],
            extras=[],
            environment_markers=None,
            hashes=None,
        ),
    ),
    (
        " packaging== 20.7 ",
        RequirementEntry(
            package="packaging",
            versions=[("==", "20.7")],
            extras=[],
            environment_markers=None,
            hashes=None,
        ),
    ),
    (
        "packaging==20.7"
        " --hash=sha256:a841dacd6b99318a741b166adb07e19ee71a274450e68237b4650ca1055ab128",
        RequirementEntry(
            package="packaging",
            versions=[("==", "20.7")],
            extras=[],
            environment_markers=None,
            hashes=[
                (
                    "sha256",
                    "a841dacd6b99318a741b166adb07e19ee71a274450e68237b4650ca1055ab128",
                )
            ],
        ),
    ),
    (
        "packaging==20.7"
        " --hash=sha256:a841dacd6b99318a741b166adb07e19ee71a274450e68237b4650ca1055ab128"
        " --hash=sha256:7d5d0167b2b1ba821647616af46a749d1c653740dd0d2415100fe26e27afdf41",
        RequirementEntry(
            package="packaging",
            versions=[("==", "20.7")],
            extras=[],
            environment_markers=None,
            hashes=[
                (
                    "sha256",
                    "a841dacd6b99318a741b166adb07e19ee71a274450e68237b4650ca1055ab128",
                ),
                (
                    "sha256",
                    "7d5d0167b2b1ba821647616af46a749d1c653740dd0d2415100fe26e27afdf41",
                ),
            ],
        ),
    ),
    (
        "packaging[quux, strange]==20.7",
        RequirementEntry(
            package="packaging",
            versions=[("==", "20.7")],
            extras=["quux", "strange"],
            environment_markers=None,
            hashes=None,
        ),
    ),
    (
        "packaging[quux, strange]==20.7"
        " --hash=sha256:a841dacd6b99318a741b166adb07e19ee71a274450e68237b4650ca1055ab128"
        " --hash=sha256:7d5d0167b2b1ba821647616af46a749d1c653740dd0d2415100fe26e27afdf41",
        RequirementEntry(
            package="packaging",
            versions=[("==", "20.7")],
            extras=["quux", "strange"],
            environment_markers=None,
            hashes=[
                (
                    "sha256",
                    "a841dacd6b99318a741b166adb07e19ee71a274450e68237b4650ca1055ab128",
                ),
                (
                    "sha256",
                    "7d5d0167b2b1ba821647616af46a749d1c653740dd0d2415100fe26e27afdf41",
                ),
            ],
        ),
    ),
    (
        "packaging==20.7; "
        'python_version >= "3.5" and python_full_version < "3.0.0"'
        ' or python_full_version >= "3.4.0" and python_version >= "3.5"',
        RequirementEntry(
            package="packaging",
            versions=[("==", "20.7")],
            extras=[],
            environment_markers=(
                "or",
                (
                    "and",
                    (">=", "python_version", "3.5"),
                    ("<", "python_full_version", "3.0.0"),
                ),
                (
                    "and",
                    (">=", "python_full_version", "3.4.0"),
                    (">=", "python_version", "3.5"),
                ),
            ),
            hashes=None,
        ),
    ),
    (
        "packaging==20.7; "
        'python_version >= "3.5" and python_full_version < "3.0.0"'
        ' or python_full_version >= "3.4.0" and python_version >= "3.5"'
        " --hash=sha256:a841dacd6b99318a741b166adb07e19ee71a274450e68237b4650ca1055ab128"
        " --hash=sha256:7d5d0167b2b1ba821647616af46a749d1c653740dd0d2415100fe26e27afdf41",
        RequirementEntry(
            package="packaging",
            versions=[("==", "20.7")],
            extras=[],
            environment_markers=(
                "or",
                (
                    "and",
                    (">=", "python_version", "3.5"),
                    ("<", "python_full_version", "3.0.0"),
                ),
                (
                    "and",
                    (">=", "python_full_version", "3.4.0"),
                    (">=", "python_version", "3.5"),
                ),
            ),
            hashes=[
                (
                    "sha256",
                    "a841dacd6b99318a741b166adb07e19ee71a274450e68237b4650ca1055ab128",
                ),
                (
                    "sha256",
                    "7d5d0167b2b1ba821647616af46a749d1c653740dd0d2415100fe26e27afdf41",
                ),
            ],
        ),
    ),
    (
        "packaging[quux, strange]==99; os_name=='os2'"
        " and (python_version<'2.7' and platform_version=='2')"
        "   --hash=sha256:7d5d0167b2b1ba821647616af46a749d1c653740dd0d2415100fe26e27afdf41",
        RequirementEntry(
            package="packaging",
            versions=[("==", "99")],
            extras=["quux", "strange"],
            environment_markers=(
                "and",
                ("==", "os_name", "os2"),
                (
                    "and",
                    ("<", "python_version", "2.7"),
                    ("==", "platform_version", "2"),
                ),
            ),
            hashes=[
                (
                    "sha256",
                    "7d5d0167b2b1ba821647616af46a749d1c653740dd0d2415100fe26e27afdf41",
                )
            ],
        ),
    ),
]


def test_parse_requirements_entry() -> None:
    """Work through different requirement scenarios."""
    for entry in tests:
        req = parse_requirements_entry(entry[0])
        assert req.package == entry[1].package
        assert req.versions == entry[1].versions
        assert req.extras == entry[1].extras
        assert req.environment_markers == entry[1].environment_markers
        assert req.hashes == entry[1].hashes


def test_parse_requirements_file_exception() -> None:
    """Check exception raised for dodgy file path."""
    with pytest.raises(ValueError):
        parse_requirements_file(Path(""))
        parse_requirements_file(Path("/i_dont_exist"))


@ALL_REQ_FILES
def test_parse_requirements_file(datafiles: py.path) -> None:
    """Perform a general parse of the test files."""
    for data_file in datafiles.listdir():
        assert len(parse_requirements_file(Path(data_file))) > 0
