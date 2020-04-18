"""Tests the config command for the default Valiant config.

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


def test_cli_config(
    app: Cli, valiant_app_title: str, valiant_version: str, valiant_license: str
) -> None:
    """Test the default output from the `config` command."""
    command = app.find("config")
    command_tester = CommandTester(command)
    result = command_tester.execute()

    assert result == 0
    output = command_tester.io.fetch_output()

    assert output.find("repositories: pypi\n")
    assert output.find("default_repository: pypi\n")
    assert output.find("logging_configuration_file: None\n")
    assert output.find("reports:  {'spdx', 'basic', 'safety'}\n")


def test_cli_config_verbose(
    app: Cli, valiant_app_title: str, valiant_version: str, valiant_license: str
) -> None:
    """Test the default output from the `config` command with -v."""
    command = app.find("config")
    command_tester = CommandTester(command)
    result = command_tester.execute("-v")

    assert result == 0
    output = command_tester.io.fetch_output()

    assert output.find("metadata:\n")
    assert output.find("{'build_results': {'dictionary': 'Read',")


def test_cli_config_debug(
    app: Cli, valiant_app_title: str, valiant_version: str, valiant_license: str
) -> None:
    """Test the default output from the `config` command with -vvv."""
    command = app.find("config")
    command_tester = CommandTester(command)
    result = command_tester.execute("-vvv")

    assert result == 0
    output = command_tester.io.fetch_output()

    assert output.find("All config data:\n")
    assert output.find("{'tool': {'valiant': {")


def test_cli_config_json(
    app: Cli, valiant_app_title: str, valiant_version: str, valiant_license: str
) -> None:
    """Test the default output from the `config` command - JSON output."""
    import json

    command = app.find("config")
    command_tester = CommandTester(command)
    result = command_tester.execute("-o json")

    assert result == 0
    output = json.loads(command_tester.io.fetch_output())
    assert "tool" in output
    assert "valiant" in output["tool"]

    info = output["tool"]["valiant"]
    assert info["default_repository"] == "pypi"
    assert sorted(info["default_reports"]) == sorted(["basic", "spdx", "safety"])
    assert not info["logging_configuration_file"]


def test_cli_config_toml(
    app: Cli, valiant_app_title: str, valiant_version: str, valiant_license: str
) -> None:
    """Test the default output from the `config` command - TOML output."""
    import toml

    command = app.find("config")
    command_tester = CommandTester(command)
    result = command_tester.execute("-o toml")

    assert result == 0
    out = command_tester.io.fetch_output()
    output = toml.loads(out)
    assert "tool" in output
    assert "valiant" in output["tool"]

    info = output["tool"]["valiant"]
    assert info["default_repository"] == "pypi"
    assert sorted(info["default_reports"]) == sorted(["basic", "spdx", "safety"])
    assert "logging_configuration_file" not in info
