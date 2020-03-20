"""Base class for report providers."""
from abc import ABC, abstractmethod

from ..package import PackageMetadata
from .model import Report, ReportProviderConfiguration, ReportProviderDetails


class BaseReportProvider(ABC):
    """Base class for report providers."""

    def __init__(self, configuration: ReportProviderConfiguration):
        """Constructor.

        Args:
            configuration: The provider's config
        """
        self._configuration = configuration

    @classmethod
    @abstractmethod
    def get_report_provider_details(cls) -> ReportProviderDetails:
        """Returns the provider details."""
        pass

    @abstractmethod
    def generate_report(self, package_metadata: PackageMetadata) -> Report:
        """Constructs the report.

        Args:
            package_metadata: containing at least the package metadata

        # noqa: DAR202
        Returns:
            The report.
        """
        pass
