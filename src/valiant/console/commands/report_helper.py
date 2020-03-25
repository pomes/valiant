"""Helper funcs for generating reports."""
from typing import List, Optional

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
                "\n---------------\n".join(
                    [f"{a.package_type}: {a.url}" for a in metadata.artifacts]
                ),
            ],
        ]
    )

    return f"""
================
Package metadata
================

{base_package_table.draw()}

"""


def create_finding_report(metadata: PackageMetadata, report: Report) -> str:
    """Reports on the findings.

    # noqa:DAR101
    # noqa:DAR201
    """
    if len(report.findings.keys()) == 0:
        findings_report = "No findings"
    else:
        findings_table = Texttable()
        findings_table.set_cols_dtype(["t", "t", "t", "t", "t", "t"])
        findings_table.set_cols_align(["c", "c", "c", "l", "l", "l"])
        findings_table.add_row(
            ["Priority", "ID", "Category", "Title", "Message", "Data"]
        )
        for finding in report.all_findings:
            data: Optional[str] = None

            if finding.data:
                data = finding.data.to_json()

            findings_table.add_row(
                [
                    finding.level.value,
                    finding.id,
                    finding.category,
                    finding.title,
                    finding.message,
                    data,
                ]
            )

        findings_report = f"""\
{findings_table.draw()}
"""
    report_title = (
        f"Report: {report.provider_details.display_name} [{metadata.coordinates}]"
    )

    return f"""\
{report_title}
{"~" * len(report_title)}

{findings_report}
"""


def create_short_report(findings: List[Finding]) -> str:
    """Produces a table of findings.

    Args:
        findings: A list of findings

    Returns:
        A nice table for you
    """
    report_table = Texttable()
    report_table.add_row(
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
