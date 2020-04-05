"""Package for the base report plugin elements."""
from pathlib import Path
from typing import Any, final

from valiant.package import PackageMetadata
from valiant.plugins import BasePlugin, PluginTypeManager
from valiant.reports import Report, ReportProviderDetails


class BaseReportPlugin(BasePlugin):
    """Base class for report plugins."""

    @final
    @classmethod
    def run(cls, **kwargs: Any) -> Report:  # pragma: no cover
        """Proxies the call to prepare_report.

        Report plugins shouldn't overload this method. Instead, provide
        your own prepare_report.

        Args:
            kwargs: The usual open slather of args

        Returns:
            The report.
        """
        return cls.prepare_report(
            package_metadata=kwargs["package_metadata"],
            configuration_dir=kwargs["configuration_dir"],
        )

    @classmethod
    def prepare_report(
        cls, package_metadata: PackageMetadata, configuration_dir: Path
    ) -> Report:
        """Does the heavy lifting and prepares the reports.

        Args:
            package_metadata: containing at least the package metadata
            configuration_dir: A likely location for config files

        # noqa: DAR202

        Returns:
            A freshly minted report

        Raises:
            NotImplementedError: Cos ya gotta overload this one
        """
        raise NotImplementedError

    @classmethod
    def report_provider_details(cls) -> ReportProviderDetails:
        """Wraps up the plugin details for use with reports."""
        return ReportProviderDetails(  # noqa: DAR201
            name=cls.name,
            vendor=cls.vendor,
            display_name=cls.display_name,
            version=cls.version,
            url=cls.url,
        )


class ReportPlugins(PluginTypeManager):
    """All of the report plugins registered through entry-points/config."""

    namespace = "valiant.report"
