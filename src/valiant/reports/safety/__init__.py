"""Integrating the Safety library.

See: https://github.com/pyupio/safety
"""
from enum import Enum
from typing import Dict, List, Optional
from safety import __author__, __version__
from safety.safety import check as safety_check, Vulnerability
from safety.util import Package as SafetyPackage

from ...package import PackageCoordinates, PackageMetadata
from .. import (
    BaseReportProvider,
    Report,
    ReportProviderDetails,
    FindingLevel,
    FindingCategory,
    Finding,
)
from valiant.log import get_logger
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
            data=VulnerabilityDictionizer(vulnerability),
            url="https://github.com/pyupio/safety-db",
        )


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
        # Prep config
        if self.configuration:
            key: Optional[str] = self.configuration.get("key", None)
            db: Optional[str] = self.configuration.get("db", None)
            ignore_ids: Optional[str] = self.configuration.get("ignore_ids", None)
        else:
            key = None
            db = None
            ignore_ids = None

        if ignore_ids:
            ignore_id_list = [id.strip() for id in ignore_ids.split(",")]
        else:
            ignore_id_list = []

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

        report = Report(SafetyReportProvider.get_report_provider_details())

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
