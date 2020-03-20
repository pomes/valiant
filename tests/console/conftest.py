"""Pytest config."""
import pytest

from _pytest.config import Config
from cleo import ApplicationTester
from valiant.console import Cli


def pytest_configure(config: Config) -> None:
    """General Pytest config."""
    config.addinivalue_line(
        "markers", "cli-prod: mark as a live cli test (one that loads real data)."
    )


@pytest.fixture
def app() -> Cli:
    """Setup a Cli instance.

    Returns:
        A Cli instance for testing
    """
    app_ = Cli()
    app_.config.set_terminate_after_run(False)

    return app_


@pytest.fixture
def app_tester(app: Cli) -> ApplicationTester:
    """Wrap a Cli instance in the cleo ApplicationTester.

    See: https://cleo.readthedocs.io/en/latest/introduction.html#testing-commands

    # noqa: DAR201
    """
    return ApplicationTester(app)
