"""Tests for the `about` command."""
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
    # print(command_tester.io.fetch_error())
    assert result == 0
