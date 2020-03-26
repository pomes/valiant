"""CLI Command: audit."""
from pathlib import Path
from typing import List, NamedTuple, Optional

from valiant.reports import Finding, ReportSet

from .base_command import BaseCommand
from .package_command import Payload
from .report_helper import (
    create_metadata_report,
    create_finding_report,
    create_short_report,
)


class AuditCommand(BaseCommand):
    """Prepares an audit on a set of requirements (not yet implemented).

    audit
        {requirements-file : The file containing a requirements list}
        {reports? : One or more reports to run (optional - default is all reports)}
        {--s|short : Single table output}
        {--o|out= : the desired output type (json)}

    The audit command expects a very basic requirements file with one line per requirement
    and each requirement pinned to a specific version (e.g. texttable==1.6.2)

    Poetry users can generate this file with:
        poetry export --without-hashes --format requirements.txt --output requirements.txt

    """

    class _RequirementsEntry(NamedTuple):
        package: str
        version: str

    def handle(self) -> Optional[int]:  # noqa: D102
        requirements = Path(self.argument("requirements-file"))
        report_list: Optional[List[str]] = None
        format = self.option("out")
        package_list: List[AuditCommand._RequirementsEntry] = []
        payloads: List[Payload] = []

        if self.argument("reports"):
            report_list = self.argument("reports").split(",")

        try:
            if not requirements.is_file():
                raise ValueError(
                    f"The requirements file ({requirements}) doesn't exist."
                )

            with open(requirements, "r") as reqs:
                for line in reqs:
                    package, version = line.strip().split("==")
                    package_list.append(
                        AuditCommand._RequirementsEntry(package, version)
                    )

            for req in package_list:
                package_metadata = self.valiant.get_package_metadata(
                    package_name=req.package, package_version=req.version,
                )
                reports = self.valiant.get_package_reports(
                    package_metadata, reports=report_list
                )
                payloads.append(
                    Payload(metadata=reports.package_metadata, reports=reports.reports)
                )

            if format == "json":
                self.line(self.to_json(payloads))
            else:
                self.line(self.to_text(payloads))

        except Exception as e:
            self.output_error(e, format=self.option("out"))
            return 1

        return 0

    def compile_all_findings(self, payloads: List[Payload]) -> List[Finding]:
        """Compiles all findings across all reports.

        Args:
            payloads: A list of payloads with reportsets

        Returns:
            A list containing all findings
        """
        from itertools import chain

        all_report_sets: List[ReportSet] = [
            payload.reports for payload in payloads if payload.reports
        ]

        return list(chain.from_iterable([rs.all_findings for rs in all_report_sets]))

    def prepare_payload_report(self, payload: Payload) -> str:
        """Draws up yer reports.

        Args:
            payload: A single package payload

        Returns:
            A nice report for you and your pals

        Raises:
            ValueError: if you forget to load the payload with the metadata and reports data
        """
        if not payload.metadata:
            raise ValueError("No package metadata available.")

        if not payload.reports:
            raise ValueError("The report set has not been provided.")

        output = create_metadata_report(payload.metadata)

        for _, report in payload.reports.items():
            output += create_finding_report(payload.metadata, report)

        return output

    def to_text(self, payloads: List[Payload]) -> str:
        """Prepares text representations.

        Args:
            payloads: A list of payloads with the package metadata and reports

        Returns:
            Text just for you.
        """
        if self.option("short"):
            output = create_short_report(self.compile_all_findings(payloads))
        else:
            outlist = []
            for payload in payloads:
                outlist.append(self.prepare_payload_report(payload))

            output = "\n".join(outlist)

        return output

    def to_json(self, payloads: List[Payload]) -> str:
        """Converts data to json."""  # noqa:DAR101,DAR201
        import json

        if self.option("short"):
            return json.dumps(
                [f.to_dict() for f in self.compile_all_findings(payloads)]
            )

        return json.dumps([p.to_dict() for p in payloads])
