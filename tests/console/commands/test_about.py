"""Tests for the `about` command."""
from cleo import CommandTester
from valiant.console import Cli


def test_cli_about(app: Cli) -> None:
    """Test the static output from the `about` command."""
    command = app.find("about")
    command_tester = CommandTester(command)
    result = command_tester.execute()

    assert result == 0
    output = command_tester.io.fetch_output()
    assert output.startswith("Valiant 0.1.0")
    assert output.find("Licence: MIT")
