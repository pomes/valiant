"""Tests for the `about` command.

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
from cleo import CommandTester
from valiant.console import Cli


def test_cli_about(
    app: Cli, valiant_app_title: str, valiant_version: str, valiant_license: str
) -> None:
    """Test the static output from the `about` command."""
    command = app.find("about")
    command_tester = CommandTester(command)
    result = command_tester.execute()

    assert result == 0
    output = command_tester.io.fetch_output()
    assert output.startswith(f"{valiant_app_title} {valiant_version}")
    assert output.find(valiant_license)


def test_cli_about_json(
    app: Cli,
    valiant_app_name: str,
    valiant_version: str,
    valiant_license: str,
    valiant_url: str,
) -> None:
    """Test the static output from the `about` command - JSON output."""
    import json

    command = app.find("about")
    command_tester = CommandTester(command)
    result = command_tester.execute(args="--out json")

    assert result == 0
    output = json.loads(command_tester.io.fetch_output())

    assert len(output) == 4
    assert output["name"] == valiant_app_name
    assert output["version"] == valiant_version
    assert output["license"] == valiant_license
    assert output["url"] == valiant_url


def test_cli_about_toml(
    app: Cli,
    valiant_app_name: str,
    valiant_version: str,
    valiant_license: str,
    valiant_url: str,
) -> None:
    """Test the static output from the `about` command - TOML output."""
    import toml

    command = app.find("about")
    command_tester = CommandTester(command)
    result = command_tester.execute(args="--out toml")

    assert result == 0
    output = toml.loads(command_tester.io.fetch_output())

    assert "tool" in output
    assert "valiant" in output["tool"]
    assert "about" in output["tool"]["valiant"]

    info = output["tool"]["valiant"]["about"]
    assert info["name"] == valiant_app_name
    assert info["version"] == valiant_version
    assert info["license"] == valiant_license
    assert info["url"] == valiant_url
