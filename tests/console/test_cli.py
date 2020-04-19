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
from cleo import ApplicationTester
from valiant.console import Cli


EXPECTED_VERSION = "0.3.0"


def test_cli_app_setup() -> None:
    """Make sure the cli is setup fine."""
    cli = Cli()
    assert cli.config.name == "valiant"
    assert cli.config.version == EXPECTED_VERSION


def test_main_succeeds(app_tester: ApplicationTester) -> None:
    """Make sure the basic cli call works - returning 0."""
    assert app_tester.execute("") == 0


def test_main_version(
    app_tester: ApplicationTester, valiant_app_title: str, valiant_version: str
) -> None:
    """Make sure the basic cli call works."""
    app_tester.execute("--version")
    expected = f"{valiant_app_title} version {valiant_version}\n"
    assert expected == app_tester.io.fetch_output()
