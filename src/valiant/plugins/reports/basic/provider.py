"""A basic package reporter.

Copyright (c) 2020 The Valiant Authors

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from enum import Enum
from pathlib import Path

from valiant.log import get_logger
from valiant.package import PackageCoordinates, PackageMetadata
from valiant.plugins.reports import BaseReportPlugin
from valiant.reports import (
    Finding,
    FindingCategory,
    FindingLevel,
    Report,
)
from valiant.util import Dictionizer


log = get_logger()


class BasicId(Enum):
    """Setup for findings."""

    LICENCE_NOT_FOUND = (
        "BASIC001",
        FindingLevel.PRIORITY,
        "No license found",
        "The project's package needs to declare a license.",
    )
    PROJECT_NOT_FOUND = (
        "BASIC002",
        FindingLevel.WARNING,
        "No link to project site",
        "The project doesn't provide a link to its project site.",
    )
    CODEBASE_NOT_FOUND = (
        "BASIC003",
        FindingLevel.WARNING,
        "No link to codebase",
        "The project doesn't provide a link to its codebase.",
    )
    ARTIFACT_NOT_SIGNED = (
        "BASIC004",
        FindingLevel.WARNING,
        "An artifact has not been signed",
        "One of the artifacts has not been signed.",
    )
    NON_PRODUCTION_RELEASE = (
        "BASIC005",
        FindingLevel.WARNING,
        "Package not production ready",
        "The project is marked as non-production ready.",
    )
    INACTIVE_RELEASE = (
        "BASIC006",
        FindingLevel.WARNING,
        "Package is marked as inactive",
        "The project is marked as inactive.",
    )

    def __init__(self, id: str, level: FindingLevel, title: str, message: str):
        """Constructor."""  # noqa: DAR101
        self.id = id
        self.title = title
        self.category = FindingCategory.PROJECT.value
        self.level = level
        self.message = message

    def generate_finding(
        self,
        coordinates: PackageCoordinates,
        message: str = None,
        data: Dictionizer = None,
        url: str = "",
    ) -> Finding:
        """Preps a finding.

        Args:
            coordinates: The package coordinates
            message: Helpful message.
            data: A Dictionizer subclass instance with additional data.
            url: A helpful link for the reader.

        Returns:
            The configured finding.
        """
        if message:
            msg = message
        else:
            msg = self.message

        return Finding(
            coordinates=coordinates,
            id=self.id,
            title=self.title,
            category=self.category,
            level=self.level,
            message=msg,
            data=data,
            url=url,
        )


class BasicReportPlugin(BaseReportPlugin):
    """Basic report provider implementation.

    Examines the package metadata and calls out any concerns.
    """

    name = "basic"
    vendor = "Valiant"
    display_name = "Basic"
    version = "0.1"
    url = ""

    @classmethod
    def prepare_report(
        cls, package_metadata: PackageMetadata, configuration_dir: Path
    ) -> Report:
        """Constructs the report.

        Args:
            package_metadata: containing at least the package metadata
            configuration_dir: A likely location for config files

        Returns:
            The report.
        """
        report = Report(cls.report_provider_details())

        if not package_metadata.license:
            report.add_finding(
                BasicId.LICENCE_NOT_FOUND.generate_finding(
                    coordinates=package_metadata.coordinates
                )
            )

        if not package_metadata.url_project:
            report.add_finding(
                BasicId.PROJECT_NOT_FOUND.generate_finding(
                    coordinates=package_metadata.coordinates
                )
            )

        if not package_metadata.url_code:
            report.add_finding(
                BasicId.CODEBASE_NOT_FOUND.generate_finding(
                    coordinates=package_metadata.coordinates
                )
            )

        for c in [
            item
            for item in package_metadata.classifiers_parsed
            if item.category == "Development Status"
        ]:
            if c.value in ["7 - Inactive"]:
                report.add_finding(
                    BasicId.INACTIVE_RELEASE.generate_finding(
                        coordinates=package_metadata.coordinates, data=c
                    )
                )
            elif c.value not in ["6 - Mature", "5 - Production/Stable"]:
                report.add_finding(
                    BasicId.NON_PRODUCTION_RELEASE.generate_finding(
                        coordinates=package_metadata.coordinates,
                        data=c,
                        message=f"The package is marked as '{c.value}'",
                    )
                )

        for item in package_metadata.artifacts:
            if not item.signed:
                report.add_finding(
                    BasicId.ARTIFACT_NOT_SIGNED.generate_finding(
                        coordinates=package_metadata.coordinates,
                        message=f"A package of type {item.package_type} has not been signed",
                        data=item,
                    )
                )

        log.info(
            f"Basic reporter located {len(report.findings)} findings"
            " for {str(package_metadata.coordinates)}",
            package_name=package_metadata.name,
            package_version=package_metadata.version,
            repository_url=package_metadata.repository_url,
        )

        return report
