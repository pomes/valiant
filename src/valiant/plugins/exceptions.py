"""Plugin-centric exceptions."""
import sys
from valiant.exceptions import ValiantException
from importlib.metadata import EntryPoint


class FailedToLoadPlugin(ValiantException):  # noqa: D101
    def __init__(
        self,
        exception: Exception,
        plugin_name: str = None,
        entry_point: EntryPoint = None,
    ):  # noqa: DAR101
        """Initialize FailedToLoadPlugin exception."""
        self.plugin_name = plugin_name
        self.original_exception = exception
        self.entry_point = entry_point

    def __str__(self):  # type: () -> str
        """Format our exception message."""  # noqa: DAR201
        return (
            f"Failed to load plugin '{self.plugin_name}' due to {self.original_exception}. "
            f"Entry point is: {self.entry_point}. "
            f"sys.path is: {sys.path}"
        )
