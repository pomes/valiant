"""Report generation functionality."""
from valiant.package import PackageMetadata

from .model import (
    Finding,
    FindingCategory,
    FindingLevel,
    NoValue,
    Report,
    ReportProviderConfiguration,
    ReportProviderDetails,
    ReportSet,
)
from .report import BaseReportProvider
from .basic import BasicReportProvider
from .spdx import SpdxLicenseReportProvider
from .safety import SafetyReportProvider


class ReportFactory:
    """Factory for generating Valiant reports."""

    from typing import Dict

    def generate_reports(
        self,
        package_metadata: PackageMetadata,
        configuration: Dict[str, ReportProviderConfiguration],
    ) -> ReportSet:
        """Generate a requested report.

        The report configuration is used to determine the report provider.

        Args:
            package_metadata: The python package metadata.
            configuration: The report providers to use.

        Returns:
            A ReportSet instance with reports for all requested providers.

        Raises:
            ValueError: When a requested provider isn't available.
        """
        reports = ReportSet()
        for provider, config in configuration.items():
            if provider == "basic":
                reports.add_report(
                    BasicReportProvider(config).generate_report(package_metadata)
                )
            elif provider == "safety":
                reports.add_report(
                    SafetyReportProvider(config).generate_report(package_metadata)
                )
            elif provider == "spdx":
                spdx = SpdxLicenseReportProvider(config)
                report = spdx.generate_report(package_metadata)
                reports.add_report(report)
            else:
                raise ValueError(
                    f"No implementation available for provider '{provider}'"
                )

        return reports
