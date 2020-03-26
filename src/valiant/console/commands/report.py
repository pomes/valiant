"""CLI Command: report."""
from .package_command import PackageCommand, Payload
from .report_helper import (
    create_short_report,
    create_metadata_report,
    create_finding_report,
)


class ReportCommand(PackageCommand):
    """Prepares a report on the package.

    report
        {package : The package name}
        {version : The package version}
        {reports? : One or more reports to run (optional - default is all reports)}
        {--r|repository= : The repository to use (not used)}
        {--s|short : Single table output}
        {--o|out= : the desired output type (json)}
    """

    def prepare_data(self) -> Payload:
        """Gets the package metadata.

        Returns:
            Package metadata

        Raises:
            ValueError: When the package data can't be loaded
        """
        package_metadata = self.valiant.get_package_metadata(
            package_name=self.argument("package"),
            package_version=self.argument("version"),
            repository_name=self.option("repository"),
        )

        if self.argument("reports"):
            report_list = self.argument("reports").split(",")
        else:
            report_list = None

        if not package_metadata:
            raise ValueError("Package details could not be loaded.")

        payload = self.valiant.get_package_reports(
            package_metadata, reports=report_list
        )

        return Payload(metadata=payload.package_metadata, reports=payload.reports)

    def to_text(self, payload: Payload) -> str:
        """Prepares text representations.

        Args:
            payload: A payload with the package metadata and reports

        Returns:
            Text just for you.

        Raises:
            ValueError: When the package metadata or reports are missing

        """
        if not payload.metadata:
            raise ValueError("No package metadata available.")

        if not payload.reports:
            raise ValueError("The report set has not been provided.")

        if self.option("short"):
            output = create_short_report(payload.reports.all_findings)
        else:
            output = create_metadata_report(payload.metadata)

            for _, report in payload.reports.items():
                output += create_finding_report(payload.metadata, report)

        return output
