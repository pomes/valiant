"""Base command for use by commands that use a basic payload."""
from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional

from valiant.package import PackageMetadata
from valiant.reports import ReportSet
from valiant.util import Dictionizer

from .base_command import BaseCommand


@dataclass(frozen=True)
class Payload(Dictionizer):
    """Utility class for passing data around."""

    metadata: Optional[PackageMetadata] = None
    reports: Optional[ReportSet] = None
    message: str = ""

    def to_dict(self) -> Dict:  # noqa:D102
        return {
            "message": self.message,
            "metadata": self.metadata.to_dict() if self.metadata else None,
            "reports": self.reports.to_dict() if self.reports else None,
        }


class PackageCommand(BaseCommand):
    """Handy general command base for use by actual commands."""

    def handle(self) -> Optional[int]:  # noqa: D102
        try:
            data = self.prepare_data()
            self.output_data(data, format=self.option("out"))
            return 0
        except Exception as e:
            self.output_error(e, format=self.option("out"))
            return 1

    @abstractmethod
    def prepare_data(self) -> Payload:
        """Subclass-based payload prep."""
        raise NotImplementedError  # noqa:DAR101,DAR401

    def output_data(self, payload: Payload, format: str = None) -> None:
        """Outputs the payload to the required format."""  # noqa:DAR101
        if format == "json":
            self.line(self.to_json(payload))
        else:
            self.line(self.to_text(payload))

    def to_text(self, payload: Payload) -> str:
        """Prepares text representations.

        Args:
            payload: The payload to display.

        Returns:
            At the very least we'll return `payload.message`.
        """
        return payload.message

    def to_json(self, payload: Payload) -> str:
        """Converts payload to json."""  # noqa:DAR101,DAR201
        import json

        if self.option("short"):
            if payload.reports:
                return json.dumps([f.to_dict() for f in payload.reports.all_findings])
            else:
                return "[]"  # empty json list

        return payload.to_json()
