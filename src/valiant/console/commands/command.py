"""Base command for use by actual commands."""
import json

from abc import abstractmethod
from typing import Any, Dict, Optional

from cleo import Command as BaseCommand
from valiant import Valiant


class Command(BaseCommand):
    """Base command for use by actual commands."""

    def handle(self) -> Optional[int]:  # noqa: D102
        try:
            data = self.prepare_data()
            self.output_data(data, format=self.option("out"))
            return 0
        except Exception as e:
            self.output_error(e, format=self.option("out"))
            return 1

    @property
    def valiant(self) -> Valiant:
        """Access the Valiant application object."""
        return self.application.valiant  # noqa: DAR201

    @abstractmethod
    def prepare_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Subclass-based data prep."""
        raise NotImplementedError  # noqa:DAR101,DAR401

    def output_error(self, e: Exception, format: str = None) -> None:
        """Outputs the error to the required format."""  # noqa:DAR101
        if format == "json":
            output = self.to_json(
                {"error": {"type": e.__class__.__name__, "message": str(e)}}
            )
        else:
            output = f"<error>{e.__class__.__name__}: {e}"

        self.line_error(output)

    def output_data(self, data: Dict[str, Any], format: str = None) -> None:
        """Outputs the data to the required format."""  # noqa:DAR101
        if format == "json":
            self.line(self.to_json(data))
        else:
            self.line(self.to_text(data))

    @abstractmethod
    def to_text(self, data: Dict[str, Any]) -> str:
        """Prepares text representations."""
        raise NotImplementedError  # noqa:DAR101,DAR401

    def to_json(self, data: Dict[str, Any]) -> str:
        """Converts data to json."""  # noqa:DAR101,DAR201
        return json.dumps(data)
