"""Tests for the `audit` command.

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
import py
import pytest

from cleo import CommandTester
from valiant.console import Cli

from . import TEST_FILE_DIR


@pytest.mark.e2e
@pytest.mark.datafiles(TEST_FILE_DIR / "requirements-small.txt")
def test_cli_audit(app: Cli, datafiles: py.path) -> None:
    """Test the static output from the `audit` command."""
    command = app.find("audit")
    command_tester = CommandTester(command)
    result = command_tester.execute(f"{datafiles / 'requirements-small.txt'}")

    assert result == 0


@pytest.mark.e2e
@pytest.mark.datafiles(TEST_FILE_DIR / "requirements-small.txt")
def test_cli_audit_short(app: Cli, datafiles: py.path) -> None:
    """Test the static output from the `audit` command."""
    command = app.find("audit")
    command_tester = CommandTester(command)
    result = command_tester.execute(f"-s {datafiles / 'requirements-small.txt'}")

    assert result == 0


@pytest.mark.e2e
@pytest.mark.datafiles(TEST_FILE_DIR / "requirements-small.txt")
def test_cli_audit_json(app: Cli, datafiles: py.path) -> None:
    """Test the output from the `audit` command - JSON output."""
    import json

    command = app.find("audit")
    command_tester = CommandTester(command)
    result = command_tester.execute(f"{datafiles / 'requirements-small.txt'} -o json")

    assert result == 0
    output = json.loads(command_tester.io.fetch_output())
    assert output
    assert len(output) == 7

    expected_packages = [
        ("click", "7.1.1"),
        ("flask", "1.1.1"),
        ("itsdangerous", "1.1.0"),
        ("jinja2", "2.11.1"),
        ("markupsafe", "1.1.1"),
        ("werkzeug", "1.0.1"),
        ("insecure-package", "0.1.0"),
    ]

    package_reports = [
        (item["metadata"]["name"].lower(), item["metadata"]["version"])
        for item in output
    ]

    assert len(package_reports) == len(expected_packages)

    for pkg in expected_packages:
        assert pkg in package_reports

    for item in output:
        assert len(item["reports"]) == 3
        assert "safety" in item["reports"]
        assert "spdx" in item["reports"]
        assert "basic" in item["reports"]


@pytest.mark.e2e
@pytest.mark.datafiles(TEST_FILE_DIR / "requirements-small.txt")
def test_cli_audit_toml(app: Cli, datafiles: py.path) -> None:
    """Test the output from the `audit` command - JSON output.

    TODO: Flesh out this test.
    """
    import toml

    command = app.find("audit")
    command_tester = CommandTester(command)
    result = command_tester.execute(f"{datafiles / 'requirements-small.txt'} -o toml")

    assert result == 0
    output = toml.loads(command_tester.io.fetch_output())
    assert output

    reports = output["tool"]["valiant"]["report"]
    assert len(reports) == 7

    expected_packages = [
        ("click", "7.1.1"),
        ("flask", "1.1.1"),
        ("itsdangerous", "1.1.0"),
        ("jinja2", "2.11.1"),
        ("markupsafe", "1.1.1"),
        ("werkzeug", "1.0.1"),
        ("insecure-package", "0.1.0"),
    ]

    package_reports = [
        (item["metadata"]["name"].lower(), item["metadata"]["version"])
        for item in reports
    ]

    assert len(package_reports) == len(expected_packages)

    for pkg in expected_packages:
        assert pkg in package_reports

    for rep in reports:
        assert len(rep["reports"]) == 3
        assert "safety" in rep["reports"]
        assert "spdx" in rep["reports"]
        assert "basic" in rep["reports"]
