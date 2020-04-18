"""Test configuration.

See: https://docs.pytest.org/en/latest/pythonpath.html

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
