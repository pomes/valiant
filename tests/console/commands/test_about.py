"""Tests for the `about` command."""
from cleo import CommandTester
from valiant.console import Cli


def test_cli_about(app: Cli) -> None:
    """Test the static output from the `about` command."""
    command = app.find("about")
    command_tester = CommandTester(command)
    result = command_tester.execute()
    expected = """\
Valiant 0.1.0 - Dependency Investigations Unit

Valiant helps you investigate dependencies

Licence: MIT
See https://github.com/pomes/valiant for more information.
"""
    assert result == 0
    assert expected == command_tester.io.fetch_output()
