"""Models for reports and report providers."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class FindingLevel(Enum):
    """A priority level."""

    PRIORITY = 0
    WARNING = 1
    INFO = 2


@dataclass(frozen=True)
class Finding:
    """A single finding note."""

    level: FindingLevel

    """A brief (<100 characters) title for the finding."""
    title: Optional[str]

    """A longer description of the finding."""
    message: str

    """A link for further details."""
    url: Optional[str]


@dataclass(frozen=True)
class ReportProviderDetails:
    """Describes the report provider."""

    name: str
    vendor: Optional[str]
    display_name: str

    """The version of the report provider."""
    version: str

    """A link for further details."""
    url: Optional[str]


@dataclass(frozen=True)
class ReportProviderConfiguration:
    """A very generic class to allow for flexible configuration."""

    items: Dict[str, Any]


class Report:
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


class ReportSet:
    """Manages a set of reports from various providers."""

    def __init__(self):
        """Constructor."""
        self._reports = Dict[str, Report]
