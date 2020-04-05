"""Demonstrator plugin."""
from pathlib import Path

from valiant.plugins.reports import (
    BaseReportPlugin,
    Finding,
    FindingCategory,
    FindingLevel,
    PackageMetadata,
    Report,
    get_logger,
)

log = get_logger()


class DemoReportPlugin(BaseReportPlugin):
    """A sample reporting plugin."""

    name = "demo"
    vendor = "Valiant"
    display_name = "Demo"
    version = "0.1"
    url = ""

    @classmethod
    def prepare_report(
        cls, package_metadata: PackageMetadata, configuration_dir: Path
    ) -> Report:
        """Run the report.

        Args:
            package_metadata: The package information
            configuration_dir: A directory for locating config

        Returns:
            A report with (perhaps) a finding or two.
        """
        report = Report(cls.report_provider_details())
        log.info(
            "The demo plugin was called",
            package_name=package_metadata.name,
            package_version=package_metadata.version,
        )
        report.add_finding(
            Finding(
                coordinates=package_metadata.coordinates,
                id="DEMO001",
                title="Demo finding",
                category=FindingCategory.PROJECT.value,
                level=FindingLevel.INFO,
                message="This is a demo finding",
                data={"value": "demo"},
                url="http://www.example.com",
            )
        )
        return report
