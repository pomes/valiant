"""Helper funcs for generating reports.

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
from typing import List

from texttable import Texttable
from valiant.package import PackageMetadata
from valiant.reports import Finding, Report


def create_metadata_report(metadata: PackageMetadata) -> str:
    """Reports on the package metadata.

    # noqa:DAR101
    # noqa:DAR201
    """
    base_package_table = Texttable()

    base_package_table.add_rows(
        [
            ["Item", "Value(s)"],
            ["Package", metadata.name],
            ["Version", metadata.version],
            ["Repository", metadata.repository_url],
            ["License", metadata.license],
            ["Summary", metadata.summary],
            [
                "Resources",
                "\n".join(
                    [
                        f"Project: {metadata.url_project}",
                        f"Code: {metadata.url_code}",
                        f"Documentation: {metadata.url_documentation}",
                        f"Issue tracker:: {metadata.url_issue_tracker}",
                    ]
                ),
            ],
            ["Classifiers", "\n".join(metadata.classifiers)],
            [
                "Artifacts",
                "\n---\n".join(
                    [f"{a.package_type}: {a.url}" for a in metadata.artifacts]
                ),
            ],
        ]
    )

    return f"<h1>Package metadata</h1>\n{base_package_table.draw()}\n\n"


def create_finding_report(metadata: PackageMetadata, report: Report) -> str:
    """Reports on the findings.

    # noqa:DAR101
    # noqa:DAR201
    """
    if len(report.findings.keys()) == 0:
        findings_report = "<comment>No findings</comment>"
    else:
        findings_table = Texttable()
        findings_table.set_cols_dtype(["t", "t", "t", "t", "t"])
        findings_table.set_cols_align(["c", "c", "c", "l", "l"])
        findings_table.header(["Priority", "ID", "Category", "Title", "Message"])
        for finding in report.all_findings:
            findings_table.add_row(
                [
                    finding.level.value,
                    finding.id,
                    finding.category,
                    finding.title,
                    finding.message,
                ]
            )

        findings_report = findings_table.draw()

    report_title = (
        f"Report: {report.provider_details.display_name} [{metadata.coordinates}]"
    )

    return f"<h1>{report_title}</h1>\n{findings_report}\n\n"


def create_short_report(findings: List[Finding]) -> str:
    """Produces a table of findings.

    Args:
        findings: A list of findings

    Returns:
        A nice table for you
    """
    if len(findings) == 0:
        return "<comment>No findings</comment>"

    report_table = Texttable()
    report_table.header(
        ["Package Coordinates", "ID", "Level", "Category", "Title", "Message"]
    )

    for finding in findings:
        report_table.add_row(
            [
                finding.coordinates,
                finding.id,
                finding.level.value,
                finding.category,
                finding.title,
                finding.message,
            ]
        )

    return report_table.draw()
