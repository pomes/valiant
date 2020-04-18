"""Tests for the demo report plugin.

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


def test_demo_report_provider_details() -> None:
    """Check the provider details."""
    from valiant.plugins.reports.demo import DemoReportPlugin

    report = DemoReportPlugin.report_provider_details()

    assert report.name == "demo"
    assert report.vendor == "Valiant"
    assert report.display_name == "Demo"
    assert report.version == "0.1"
    assert report.url == ""


def test_demo_report() -> None:
    """Check theonly finding that demo produces."""
    from valiant.reports import FindingLevel
    from valiant.plugins.reports.demo import DemoReportPlugin
    from valiant.repositories.pypi import PyPiPackageMetadata

    from data.basic_package import BASIC_PACKAGE

    metadata = PyPiPackageMetadata(
        repository_url="https://pypi.example.com", package_data=BASIC_PACKAGE
    )

    report = DemoReportPlugin.prepare_report(
        package_metadata=metadata, configuration_dir=None
    )
    assert len(report.findings) == 1

    finding = report.all_findings[0]

    assert finding.id == "DEMO001"
    assert finding.title == "Demo finding"
    assert finding.level == FindingLevel.INFO
    assert finding.category == "project"
    assert finding.message == "This is a demo finding"
    assert finding.url == "http://www.example.com"
    assert finding.data["value"] == "demo"
