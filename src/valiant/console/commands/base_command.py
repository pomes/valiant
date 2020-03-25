"""A helpful base to get started from."""
import json
import traceback

from cleo import Command as CleoCommand
from clikit.api.io.flags import VERBOSE

from valiant import Valiant


class BaseCommand(CleoCommand):
    """Common methods for most commands."""

    @property
    def valiant(self) -> Valiant:
        """Access the Valiant application object."""
        return self.application.valiant  # noqa: DAR201

    def output_error(self, e: Exception, format: str = None) -> None:
        """Outputs the error to the required format."""  # noqa:DAR101
        if format == "json":
            data = {"error": {"type": e.__class__.__name__, "message": str(e)}}
            if self.io.is_verbose():
                data["error"]["trace"] = traceback.format_exc()
            self.line_error(json.dumps(data))
        else:
            output = f"<error>{e.__class__.__name__}: {e}\n"
            self.line_error(output)
            if self.io.is_verbose():
                self.line_error(
                    f"<debug>{traceback.format_exc()}</debug>", verbosity=VERBOSE
                )
