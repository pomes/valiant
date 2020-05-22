"""Tests for the `report` command.

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
import pytest

from cleo import CommandTester
from valiant.console import Cli


@pytest.mark.e2e
def test_cli_report(app: Cli) -> None:
    """Test the static output from the `report` command."""
    command = app.find("report")
    command_tester = CommandTester(command)
    result = command_tester.execute("flask 1.1.1")

    assert result == 0


@pytest.mark.e2e
def test_cli_report_short(app: Cli) -> None:
    """Test the static output from the `report` command."""
    command = app.find("report")
    command_tester = CommandTester(command)
    result = command_tester.execute("-s flask 1.1.1")

    assert result == 0


@pytest.mark.e2e
def test_cli_report_json(app: Cli) -> None:
    """Test the output from the `report` command - JSON output."""
    import json

    command = app.find("report")
    command_tester = CommandTester(command)
    result = command_tester.execute("flask 1.1.1 -o json")

    assert result == 0
    output = json.loads(command_tester.io.fetch_output())
    assert output

    assert output["metadata"]["name"].lower() == "flask"
    assert output["metadata"]["version"] == "1.1.1"

    assert len(output["reports"]) == 3
    assert "safety" in output["reports"]
    assert "spdx" in output["reports"]
    assert "basic" in output["reports"]


@pytest.mark.e2e
def test_cli_report_toml(app: Cli) -> None:
    """Test the output from the `report` command - TOML output."""
    import toml

    command = app.find("report")
    command_tester = CommandTester(command)
    result = command_tester.execute("flask 1.1.1 -o toml")

    assert result == 0
    output = toml.loads(command_tester.io.fetch_output())
    assert output

    metadata = output["tool"]["valiant"]["report"]["metadata"]
    assert metadata["name"].lower() == "flask"
    assert metadata["version"] == "1.1.1"

    reports = output["tool"]["valiant"]["report"]["reports"]
    assert len(reports) == 3
    assert "safety" in reports
    assert "spdx" in reports
    assert "basic" in reports
