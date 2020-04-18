"""Models for reports and report providers.

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
from dataclasses import dataclass
from datetime import datetime
from typing import cast, Dict, Iterable, List, Mapping, Optional, Tuple, Union

from valiant.package import PackageCoordinates
from valiant.util import Dictionizer, NoValue


class FindingLevel(NoValue):
    """A priority level."""

    PRIORITY = "priority"
    WARNING = "warning"
    INFO = "info"


class FindingCategory(NoValue):
    """A useful set of finding categories.

    This is just a helper and you should use the value
    of the member/instance (FindingCategory.SECURITY.value).
    """

    SECURITY = "security"
    LICENSE = "license"
    PROJECT = "project"


@dataclass(frozen=True)
class Finding(Dictionizer):
    """A single finding note."""

    coordinates: PackageCoordinates

    """ An identifier for the finding.

    Please use the provider name (in uppercase) followed by a 3-digit identifier
    such as 001 and 078. Examples include:
        - BASIC001
        - SPDX021
        - SAFETY004
    """
    id: str

    """An appropriate priority for this finding."""
    level: FindingLevel

    """An open category.

    Where possible, use FindingCategory values (e.g. FindingCategory.SECURITY.value)."""
    category: str

    """A brief (<100 characters) title for the finding."""
    title: Optional[str]

    """A longer description of the finding."""
    message: str

    """Allows report providers to optionally add further data."""
    data: Optional[Union[Mapping, Dictionizer]]

    """A link for further details."""
    url: Optional[str]

    def to_dict(self) -> Dict:  # noqa:D102
        data: Mapping = {}

        if self.data:
            if hasattr(self.data, "to_dict"):
                data = cast(Dictionizer, self.data).to_dict()
            else:
                data = cast(Mapping, self.data)

        return {
            "id": self.id,
            "coordinates": self.coordinates.to_dict(),
            "level": self.level.value,
            "category": self.category,
            "title": self.title,
            "message": self.message,
            "data": data,
            "url": self.url,
        }


@dataclass(frozen=True)
class ReportProviderDetails(Dictionizer):
    """Describes the report provider."""

    name: str
    vendor: Optional[str]
    display_name: str

    """The version of the report provider."""
    version: str

    """A link for further details."""
    url: Optional[str]

    def to_dict(self) -> Dict:  # noqa:D102
        return {
            "name": self.name,
            "vendor": self.vendor,
            "display_name": self.display_name,
            "version": self.version,
            "url": self.url,
        }


class Report(Dictionizer):
    """An individual report from a report provider."""

    def __init__(self, provider_details: ReportProviderDetails):
        """Constructor.

        Args:
            provider_details: The provider's details.
        """
        self._findings: Dict[FindingLevel, List[Finding]] = {}

        self._created: datetime = datetime.now()
        self._provider: ReportProviderDetails = provider_details

    def add_finding(self, finding: Finding) -> None:
        """Add a finding to the list."""  # noqa:DAR101
        if finding.level not in self._findings:
            self._findings[finding.level] = [finding]
        else:
            self._findings[finding.level].append(finding)

    def add_findings(self, findings: List[Finding]) -> None:
        """Add a finding to the list."""  # noqa:DAR101
        for finding in findings:
            self.add_finding(finding)

    @property
    def created(self) -> datetime:  # noqa:D102
        return self._created

    @property
    def provider_details(self) -> ReportProviderDetails:  # noqa:D102
        return self._provider

    @property
    def findings(self) -> Dict[FindingLevel, List[Finding]]:  # noqa:D102
        return self._findings

    @property
    def all_findings(self) -> List[Finding]:  # noqa:D102
        from itertools import chain

        return list(chain.from_iterable(self._findings.values()))

    def to_dict(self) -> Dict:  # noqa:D102
        return {
            "created": self.created.isoformat(),
            "provider": self.provider_details.to_dict(),
            "findings": [finding.to_dict() for finding in self.all_findings],
        }


class ReportSet(Dictionizer):
    """Manages a set of reports from various providers."""

    def __init__(self):
        """Constructor."""
        self._reports: Dict[str, Report] = {}

    def add_report(self, report: Report) -> None:
        """Add a single report to the set.

        Args:
            report: The report to add (no, really)

        Raises:
            ValueError: when the `report.provider_details.name` has
                        already filed a report
        """
        name = report.provider_details.name
        if name in self._reports:
            raise ValueError(f"The provider {name} already has a report in the set.")

        self._reports[name] = report

    def items(self) -> Iterable[Tuple[str, Report]]:
        """Lets you iterate over the reports in the set.

        Returns:
            As for a dictionary
        """
        return self._reports.items()

    @property
    def all_findings(self) -> List[Finding]:
        """Get all findings across the reports.

        Returns:
            A list of all findings from across all reports in the set.
        """
        from itertools import chain

        return list(
            chain.from_iterable(
                [report.all_findings for report in self._reports.values()]
            )
        )

    def to_dict(self) -> Dict:  # noqa:D102
        return {name: report.to_dict() for name, report in self._reports.items()}
