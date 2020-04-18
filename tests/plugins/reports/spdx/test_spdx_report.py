"""Tests for the spdx report plugin.

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


def test_spdx_report_provider_details() -> None:
    """Check the provider details."""
    from valiant.plugins.reports.spdx import SpdxLicenseReportPlugin

    report = SpdxLicenseReportPlugin.report_provider_details()

    assert report.name == "spdx"
    assert report.vendor == "Valiant"
    assert report.display_name == "SPDX License"
    assert report.version == "0.1"
    assert report.url == "https://spdx.org/licenses/"


def test_spdx_report() -> None:
    """Check there are no adverse findings on a well-covered package."""
    from valiant.plugins.reports.spdx import SpdxLicenseReportPlugin
    from valiant.reports import FindingLevel
    from valiant.repositories.pypi import PyPiPackageMetadata

    from .data.basic_package import PACKAGE

    metadata = PyPiPackageMetadata(
        repository_url="https://pypi.example.com", package_data=PACKAGE
    )

    report = SpdxLicenseReportPlugin.prepare_report(
        package_metadata=metadata, configuration_dir=None
    )
    assert len(report.all_findings) == 1

    assert report.all_findings[0].id == "SPDX001"
    assert report.all_findings[0].level == FindingLevel.INFO
    assert report.all_findings[0].category == "license"
    assert report.all_findings[0].title == "SPDX License found"
    data = report.all_findings[0].data

    assert data["name"] == "MIT License"
    assert data["id"] == "MIT"
    assert data["reference_number"] == "256"
    assert data["details_url"] == "http://spdx.org/licenses/MIT.json"


def test_spdx_report_non_spdx_license() -> None:
    """Check findings on a package with an unknown licence."""
    from valiant.plugins.reports.spdx import SpdxLicenseReportPlugin
    from valiant.reports import FindingLevel
    from valiant.repositories.pypi import PyPiPackageMetadata

    from .data.package_non_spdx import PACKAGE

    metadata = PyPiPackageMetadata(
        repository_url="https://pypi.example.com", package_data=PACKAGE
    )

    report = SpdxLicenseReportPlugin.prepare_report(
        package_metadata=metadata, configuration_dir=None
    )
    assert len(report.all_findings) == 1

    assert report.all_findings[0].id == "SPDX002"
    assert report.all_findings[0].level == FindingLevel.INFO
    assert report.all_findings[0].category == "license"
    assert report.all_findings[0].title == "SPDX License not found"
    data = report.all_findings[0].data
    assert data["original"] == "License :: I AM NOT REAL"


def test_spdx_report_deprecated_license() -> None:
    """Check findings on a package with a deprecated licence."""  # noqa: DAR401
    from valiant.plugins.reports.spdx import SpdxLicenseReportPlugin
    from valiant.reports import FindingLevel
    from valiant.repositories.pypi import PyPiPackageMetadata

    from .data.package_deprecated import PACKAGE

    metadata = PyPiPackageMetadata(
        repository_url="https://pypi.example.com", package_data=PACKAGE
    )

    report = SpdxLicenseReportPlugin.prepare_report(
        package_metadata=metadata, configuration_dir=None
    )
    assert len(report.all_findings) >= 2

    for finding in report.all_findings:
        if finding.id == "SPDX003":
            assert finding.level == FindingLevel.WARNING
            assert finding.category == "license"
            assert finding.title == "Deprecated license"
            return

    raise AssertionError("Test failed to validate finding.")
