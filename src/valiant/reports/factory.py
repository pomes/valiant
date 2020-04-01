"""Report generation functionality."""
from typing import Set

from valiant.package import PackageMetadata


from .model import ReportSet


class ReportFactory:
    """Factory for generating Valiant reports."""

    def generate_reports(
        self, report_list: Set[str], package_metadata: PackageMetadata
    ) -> ReportSet:
        """Generate a requested report.

        The report configuration is used to determine the report provider.

        Args:
            report_list: The reports to run.
            package_metadata: The python package metadata.

        Returns:
            A ReportSet instance with reports for all requested providers.

        Raises:
            ValueError: When a requested provider isn't available.
        """
        from valiant.reports.basic import BasicReportProvider
        from valiant.reports.safety import SafetyReportProvider
        from valiant.reports.spdx import SpdxLicenseReportProvider

        reports = ReportSet()
        for provider in report_list:
            if provider == "basic":
                reports.add_report(
                    BasicReportProvider().generate_report(package_metadata)
                )
            elif provider == "safety":
                reports.add_report(
                    SafetyReportProvider().generate_report(package_metadata)
                )
            elif provider == "spdx":
                spdx = SpdxLicenseReportProvider()
                report = spdx.generate_report(package_metadata)
                reports.add_report(report)
            else:
                raise ValueError(
                    f"No implementation available for provider '{provider}'"
                )

        return reports
