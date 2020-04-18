"""Tests for the basic report plugin.

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


def test_basic_report_provider_details() -> None:
    """Check the provider details."""
    from valiant.plugins.reports.basic import BasicReportPlugin

    report = BasicReportPlugin.report_provider_details()

    assert report.name == "basic"
    assert report.vendor == "Valiant"
    assert report.display_name == "Basic"
    assert report.version == "0.1"
    assert report.url == ""


def test_basic_report() -> None:
    """Check there are no findings on a well-covered package."""
    from valiant.plugins.reports.basic import BasicReportPlugin
    from valiant.repositories.pypi import PyPiPackageMetadata

    from data.basic_package import BASIC_PACKAGE

    metadata = PyPiPackageMetadata(
        repository_url="https://pypi.example.com", package_data=BASIC_PACKAGE
    )

    report = BasicReportPlugin.prepare_report(
        package_metadata=metadata, configuration_dir=None
    )
    assert len(report.findings) == 0


def test_basic_report_no_licence() -> None:
    """Check a missing licence is reported."""
    from valiant.reports import FindingCategory, FindingLevel
    from valiant.plugins.reports.basic import BasicReportPlugin
    from valiant.plugins.reports.basic.provider import BasicId
    from valiant.repositories.pypi import PyPiPackageMetadata

    from data.package_no_licence import NO_LICENSE_PACKAGE

    metadata = PyPiPackageMetadata(
        repository_url="https://pypi.example.com", package_data=NO_LICENSE_PACKAGE
    )

    report = BasicReportPlugin.prepare_report(
        package_metadata=metadata, configuration_dir=None
    )

    assert len(report.findings) == 1

    for finding in report.all_findings:
        if finding.id == BasicId.LICENCE_NOT_FOUND.id:
            assert finding.level == FindingLevel.PRIORITY
            assert finding.category == FindingCategory.PROJECT.value
            assert finding.title == "No license found"
            return

    assert False  # noqa:B011


def test_basic_report_project_not_found() -> None:
    """Check a missing project link is reported."""
    from valiant.reports import FindingCategory, FindingLevel
    from valiant.plugins.reports.basic import BasicReportPlugin
    from valiant.plugins.reports.basic.provider import BasicId
    from valiant.repositories.pypi import PyPiPackageMetadata

    from data.package_no_project import NO_PROJECT_PACKAGE

    metadata = PyPiPackageMetadata(
        repository_url="https://pypi.example.com", package_data=NO_PROJECT_PACKAGE
    )

    report = BasicReportPlugin.prepare_report(
        package_metadata=metadata, configuration_dir=None
    )

    assert len(report.findings) == 1

    for finding in report.all_findings:
        if finding.id == BasicId.PROJECT_NOT_FOUND.id:
            assert finding.level == FindingLevel.WARNING
            assert finding.category == FindingCategory.PROJECT.value
            assert finding.title == "No link to project site"
            return

    assert False  # noqa:B011


def test_basic_report_codebase_not_found() -> None:
    """Check a missing codebase link is reported."""
    from valiant.reports import FindingCategory, FindingLevel
    from valiant.plugins.reports.basic import BasicReportPlugin
    from valiant.plugins.reports.basic.provider import BasicId
    from valiant.repositories.pypi import PyPiPackageMetadata

    from data.package_no_codebase import PACKAGE

    metadata = PyPiPackageMetadata(
        repository_url="https://pypi.example.com", package_data=PACKAGE
    )

    report = BasicReportPlugin.prepare_report(
        package_metadata=metadata, configuration_dir=None
    )

    assert len(report.findings) == 1

    for finding in report.all_findings:
        if finding.id == BasicId.CODEBASE_NOT_FOUND.id:
            assert finding.level == FindingLevel.WARNING
            assert finding.category == FindingCategory.PROJECT.value
            assert finding.title == "No link to codebase"
            return

    assert False  # noqa:B011


def test_basic_report_inactive_release() -> None:
    """Check an inactive release is reported."""
    from valiant.reports import FindingCategory, FindingLevel
    from valiant.plugins.reports.basic import BasicReportPlugin
    from valiant.plugins.reports.basic.provider import BasicId
    from valiant.repositories.pypi import PyPiPackageMetadata

    from data.package_inactive import PACKAGE

    metadata = PyPiPackageMetadata(
        repository_url="https://pypi.example.com", package_data=PACKAGE
    )

    report = BasicReportPlugin.prepare_report(
        package_metadata=metadata, configuration_dir=None
    )

    assert len(report.findings) == 1

    for finding in report.all_findings:
        if finding.id == BasicId.INACTIVE_RELEASE.id:
            assert finding.level == FindingLevel.WARNING
            assert finding.category == FindingCategory.PROJECT.value
            assert finding.title == "Package is marked as inactive"
            return

    assert False  # noqa:B011


def test_basic_report_dev_release() -> None:
    """Check a dev release is reported."""
    from valiant.reports import FindingCategory, FindingLevel
    from valiant.plugins.reports.basic import BasicReportPlugin
    from valiant.plugins.reports.basic.provider import BasicId
    from valiant.repositories.pypi import PyPiPackageMetadata

    from data.package_dev import PACKAGE

    metadata = PyPiPackageMetadata(
        repository_url="https://pypi.example.com", package_data=PACKAGE
    )

    report = BasicReportPlugin.prepare_report(
        package_metadata=metadata, configuration_dir=None
    )

    assert len(report.findings) == 1

    for finding in report.all_findings:
        if finding.id == BasicId.NON_PRODUCTION_RELEASE.id:
            assert finding.level == FindingLevel.WARNING
            assert finding.category == FindingCategory.PROJECT.value
            assert finding.title == "Package not production ready"
            return

    assert False  # noqa:B011


def test_basic_report_artifact_not_signed() -> None:
    """Check an unsigned artifact is reported."""
    from valiant.reports import FindingCategory, FindingLevel
    from valiant.plugins.reports.basic import BasicReportPlugin
    from valiant.plugins.reports.basic.provider import BasicId
    from valiant.repositories.pypi import PyPiPackageMetadata

    from data.package_not_signed import PACKAGE

    metadata = PyPiPackageMetadata(
        repository_url="https://pypi.example.com", package_data=PACKAGE
    )

    report = BasicReportPlugin.prepare_report(
        package_metadata=metadata, configuration_dir=None
    )

    assert len(report.findings) == 1

    for finding in report.all_findings:
        if finding.id == BasicId.ARTIFACT_NOT_SIGNED.id:
            assert finding.level == FindingLevel.WARNING
            assert finding.category == FindingCategory.PROJECT.value
            assert finding.title == "An artifact has not been signed"
            return

    assert False  # noqa:B011
