"""The Safety provider."""
# from safety import

from safety import __author__, __version__

from ...package import PackageMetadata
from .. import BaseReportProvider, Report, ReportProviderDetails


class SafetyReportProvider(BaseReportProvider):
    """Provider implementation."""

    @classmethod
    def get_report_provider_details(cls) -> ReportProviderDetails:
        """Returns the provider details."""
        return ReportProviderDetails(  # noqa: DAR201
            name="safety",
            vendor=__author__,
            display_name="Safety",
            version=__version__,
            url="https://pyup.io/safety/",
        )

    def generate_report(self, package_metadata: PackageMetadata) -> Report:
        """Constructs the report.

        Args:
            package_metadata: containing at least the package metadata

        Returns:
            The report.
        """
        return Report(SafetyReportProvider.get_report_provider_details())
