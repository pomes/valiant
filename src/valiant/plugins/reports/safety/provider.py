"""Integrating the Safety library.

Integrating the Safety library.

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
import os

from enum import Enum
from pathlib import Path
from typing import Dict, List

from safety import __author__ as safety_author
from safety import __version__ as safety_version
from safety.safety import Vulnerability
from safety.safety import check as safety_check
from safety.util import Package as SafetyPackage
from valiant.log import get_logger
from valiant.package import PackageCoordinates, PackageMetadata
from valiant.plugins.reports import BaseReportPlugin
from valiant.reports import Finding, FindingCategory, FindingLevel, Report
from valiant.util import Dictionizer


log = get_logger()


class VulnerabilityDictionizer(Dictionizer):
    """A wrapper for Vulnerability to allow dict and json transforms."""

    def __init__(self, vulnerability: Vulnerability):
        """Constructor."""  # noqa:DAR101
        self._vulnerability = vulnerability

    def to_dict(self) -> Dict:  # noqa:DAR201
        return self._vulnerability._asdict()


class SafetyId(Enum):
    """Setup for findings."""

    VULNERABILITY_FOUND = "SAFETY001"

    def __init__(self, id: str):
        """Constructor."""  # noqa: DAR101
        self.id = id
        self.category = FindingCategory.SECURITY.value
        self.level = FindingLevel.PRIORITY

    def generate_finding(
        self, coordinates: PackageCoordinates, vulnerability: Vulnerability
    ) -> Finding:
        """Preps a finding.

        Args:
            coordinates: The package coordinates
            vulnerability: A vulnerability found by Safety

        Returns:
            The configured finding.
        """
        return Finding(
            coordinates=coordinates,
            id=self.id,
            category=self.category,
            level=self.level,
            title="Vulnerability found",
            message=vulnerability.advisory,
            data=VulnerabilityDictionizer(vulnerability).to_dict(),
            url="https://github.com/pyupio/safety-db",
        )


class SafetyReportPlugin(BaseReportPlugin):
    """Provider implementation."""

    name = "safety"
    vendor = safety_author
    display_name = "Safety"
    version = safety_version
    url = "https://pyup.io/safety/"

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
        # Prep config
        """
        if self.configuration:
            key: Optional[str] = self.configuration.get("key", None)
            db: Optional[str] = self.configuration.get("db", None)
            ignore_ids: Optional[str] = self.configuration.get("ignore_ids", None)
        else:
            key = None
            db = None
            ignore_ids = None
        """
        key = os.getenv("SAFETY_API_KEY", None)
        db = None
        ignore_ids = os.getenv("SAFETY_IGNORE_IDS", None)
        ignore_id_list: List[str] = []

        if ignore_ids:
            ignore_id_list = [id.strip() for id in ignore_ids.split(",")]

        packages = [
            SafetyPackage(key=package_metadata.name, version=package_metadata.version)
        ]

        vulnerabilities: List[Vulnerability] = safety_check(
            packages=packages,
            key=key,
            db_mirror=db,
            cached=False,
            ignore_ids=ignore_id_list,
            proxy=None,
        )

        report = Report(cls.report_provider_details())

        for v in vulnerabilities:
            report.add_finding(
                SafetyId.VULNERABILITY_FOUND.generate_finding(
                    package_metadata.coordinates, v
                )
            )

        log.info(
            f"Safety reporter located {len(report.findings)} findings"
            f" for {str(package_metadata.coordinates)}",
            package_name=package_metadata.name,
            package_version=package_metadata.version,
            repository_url=package_metadata.repository_url,
        )

        return report
