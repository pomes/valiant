"""Tests the safety plugin using the real safety data.

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
from dataclasses import dataclass

import pytest

from valiant.package import PackageCoordinates
from valiant.plugins.reports.safety import SafetyReportPlugin


@dataclass
class InsecurePackage:
    """A small pkg definition using the handy insecure-package."""

    name: str = "insecure-package"
    version: str = "0.1.0"
    repository_url: str = "https://pypi.org"

    @property
    def coordinates(self) -> str:  # noqa:D102
        return PackageCoordinates(
            name=self.name, version=self.version, repository_url=self.repository_url
        )


@pytest.mark.e2e
def test_safety_generate_report() -> None:
    """Test the generate_report method."""
    from valiant.reports import FindingLevel

    rp = SafetyReportPlugin()
    report = rp.prepare_report(InsecurePackage(), "")
    assert len(report.all_findings) == 1

    assert report.all_findings[0].id == "SAFETY001"
    assert report.all_findings[0].level == FindingLevel.PRIORITY
    assert report.all_findings[0].category == "security"
    assert report.all_findings[0].title == "Vulnerability found"
    data = report.all_findings[0].data
    assert data["vuln_id"] == "25853"


@pytest.mark.e2e
def test_safety_generate_report_with_ignore_ids() -> None:
    """Test the generate_report method."""
    import os

    os.environ["SAFETY_IGNORE_IDS"] = "25853"

    rp = SafetyReportPlugin()
    report = rp.prepare_report(InsecurePackage(), "")
    assert len(report.all_findings) == 0
