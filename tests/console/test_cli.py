"""Tests for the `about` command."""
from cleo import ApplicationTester
from valiant.console import Cli


# TODO: Add in Valiant configuration tests when config setup is ready

EXPECTED_VERSION = "0.2.0"


def test_cli_app_setup() -> None:
    """Make sure the cli is setup fine."""
    cli = Cli()
    assert cli.config.name == "valiant"
    assert cli.config.version == EXPECTED_VERSION
    assert cli.valiant.application_version == EXPECTED_VERSION


def test_main_succeeds(app_tester: ApplicationTester) -> None:
    """Make sure the basic cli call works - returning 0."""
    assert app_tester.execute("") == 0


def test_main_version(app_tester: ApplicationTester) -> None:
    """Make sure the basic cli call works."""
    app_tester.execute("--version")
    expected = f"Valiant version {EXPECTED_VERSION}\n"
    assert expected == app_tester.io.fetch_output()
