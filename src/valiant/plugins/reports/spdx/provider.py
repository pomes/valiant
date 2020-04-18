"""Report provider relating to SPDX (https://spdx.org/about).

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
from typing import List

from valiant.log import get_logger
from valiant.package import (
    CLASSIFIER_CATEGORY_LICENSE,
    Classifier,
    PackageCoordinates,
    PackageMetadata,
)
from valiant.plugins.reports import BaseReportPlugin
from valiant.reports import Finding, FindingCategory, FindingLevel, Report
from valiant.util import Dictionizer

from .license import SpdxLicenses


SPDX_LICENCES = SpdxLicenses.builtin_loader()

log = get_logger()


class SpdxId(Enum):
    """Setup for findings."""

    FOUND = ("SPDX001", "SPDX License found", FindingLevel.INFO)
    NOT_FOUND = ("SPDX002", "SPDX License not found", FindingLevel.INFO)
    DEPRECATED = ("SPDX003", "Deprecated license", FindingLevel.WARNING)
    NOT_OSI_APPROVED = (
        "SPDX004",
        "License not OSI approved",
        FindingLevel.INFO,
        "https://opensource.org/licenses",
    )
    NOT_FSF_FREE = (
        "SPDX005",
        "License not FSF free software",
        FindingLevel.INFO,
        "https://www.gnu.org/licenses/license-list.html",
    )

    def __init__(  # noqa:D107
        self,
        id: str,
        title: str,
        level: FindingLevel,
        url: str = "https://spdx.org/licenses/",
    ):
        self.id = id
        self.title = title
        self.category = FindingCategory.LICENSE.value
        self.level = level
        self.url = url

    def generate_finding(
        self,
        coordinates: PackageCoordinates,
        message: str,
        data: Dictionizer = None,
        url: str = "",
    ) -> Finding:
        """Preps a finding.

        Args:
            coordinates: The package coordinates
            message: The finding message.
            data: Supplemental data.
            url: A link to help the reader.

        Returns:
            The configured finding.
        """
        if data:
            data_map = data.to_dict()
        else:
            data_map = {}

        return Finding(
            coordinates=coordinates,
            id=self.id,
            title=self.title,
            category=self.category,
            level=self.level,
            message=message,
            data=data_map,
            url=url if url else self.url,
        )


class SpdxLicenseReportPlugin(BaseReportPlugin):
    """SPDX License report provider implementation.

    Attempts to match the license provided in package metadata to
    an SPDX license.
    """

    name = "spdx"
    vendor = "Valiant"
    display_name = "SPDX License"
    version = "0.1"
    url = "https://spdx.org/licenses/"

    @staticmethod
    def _extract_licences_from_metadata(
        package_metadata: PackageMetadata,
    ) -> List[Classifier]:
        candidates: List[Classifier] = []

        if package_metadata.license:
            candidates.append(
                Classifier(
                    original=f"{CLASSIFIER_CATEGORY_LICENSE} :: {package_metadata.license}",
                    category=CLASSIFIER_CATEGORY_LICENSE,
                    subcategories=[],
                    value=package_metadata.license,
                )
            )

        """
        TODO: It might be possible to map the classifiers back to a license code but
              my initial analysis indicated that the classifier info is too coarse

        for item in [
            classifier
            for classifier in package_metadata.classifiers_parsed
            if classifier.category == CLASSIFIER_CATEGORY_LICENSE
        ]:
            candidates.append(item)
        """

        return candidates

    @staticmethod
    def _map_to_spdx(
        package_metadata: PackageMetadata, candidates: List[Classifier]
    ) -> List[Finding]:
        findings: List[Finding] = []

        for item in candidates:
            match = SPDX_LICENCES.get_license(item.value)
            if match:
                findings.append(
                    SpdxId.FOUND.generate_finding(
                        package_metadata.coordinates,
                        message=match.id,
                        data=match,
                        url=match.details_url,
                    )
                )
                if not match.is_osi_approved:
                    findings.append(
                        SpdxId.NOT_OSI_APPROVED.generate_finding(
                            package_metadata.coordinates,
                            message=f"License '{match.id}' is not OSI-approved.",
                        )
                    )
                if not match.is_fsf_libre:
                    findings.append(
                        SpdxId.NOT_FSF_FREE.generate_finding(
                            package_metadata.coordinates,
                            message=f"License '{match.id}' is not FSF-approved.",
                        )
                    )
                if match.is_deprecated:
                    findings.append(
                        SpdxId.DEPRECATED.generate_finding(
                            package_metadata.coordinates,
                            message=f"License '{match.id}' is deprecated.",
                        )
                    )
            else:
                findings.append(
                    SpdxId.NOT_FOUND.generate_finding(
                        package_metadata.coordinates,
                        message=f"Could not map licence {item.value} to an SPDX license",
                        data=item,
                        url="https://spdx.org/licenses/",
                    )
                )

        return findings

    @staticmethod
    def map_package_license_to_spdx(
        package_metadata: PackageMetadata,
    ) -> List[Finding]:
        """Attempts to map all licence info to SPDX licenses.

        Args:
            package_metadata: The package to review.

        Returns:
            A list of findings. Some will provide a mapping others will not.
        """
        candidates = SpdxLicenseReportPlugin._extract_licences_from_metadata(
            package_metadata
        )

        if len(candidates) == 0:
            return []

        return SpdxLicenseReportPlugin._map_to_spdx(package_metadata, candidates)

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
        report.add_findings(
            SpdxLicenseReportPlugin.map_package_license_to_spdx(package_metadata)
        )

        log.info(
            f"SPDX reporter located {len(report.findings)} findings"
            f"for {str(package_metadata.coordinates)}",
            package_name=package_metadata.name,
            package_version=package_metadata.version,
            repository_url=package_metadata.repository_url,
        )

        return report
