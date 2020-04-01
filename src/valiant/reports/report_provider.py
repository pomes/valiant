"""Base class for report providers."""
from abc import ABC, abstractmethod

from ..package import PackageMetadata
from .model import Report, ReportProviderDetails


class BaseReportProvider(ABC):
    """Base class for report providers."""

    @classmethod
    @abstractmethod
    def get_report_provider_details(cls) -> ReportProviderDetails:  # pragma: no cover
        """Returns the provider details."""
        pass

    @abstractmethod
    def generate_report(
        self, package_metadata: PackageMetadata
    ) -> Report:  # pragma: no cover
        """Constructs the report.

        Args:
            package_metadata: containing at least the package metadata

        # noqa: DAR202
        Returns:
            The report.
        """
        pass
