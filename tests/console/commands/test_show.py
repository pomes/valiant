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
import pytest

from cleo import CommandTester
from clikit.api.args.exceptions import CannotParseArgsException
from valiant.console import Cli


def test_cli_show_no_params(app: Cli) -> None:
    """Test `show` command: no params provided."""
    command = app.find("show")
    command_tester = CommandTester(command)

    with pytest.raises(CannotParseArgsException):
        result = command_tester.execute()
        assert result != 0


def test_cli_show_one_param(app: Cli) -> None:
    """Test `show` command: only one param provided."""
    command = app.find("show")
    command_tester = CommandTester(command)

    with pytest.raises(CannotParseArgsException):
        result = command_tester.execute("bottle")
        assert result != 0


def test_cli_show_not_found(app: Cli) -> None:
    """Test `show` command: package not found."""
    command = app.find("show")
    command_tester = CommandTester(command)

    result = command_tester.execute("flask 99999")
    assert result == 1


def test_cli_show_package_found(app: Cli) -> None:
    """Test `show` command: package found."""
    command = app.find("show")
    command_tester = CommandTester(command)

    result = command_tester.execute("flask 1.1.1 -v")
    assert result == 0
