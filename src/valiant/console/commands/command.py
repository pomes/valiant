"""Base command for use by actual commands."""
from cleo import Command as BaseCommand

from valiant import Valiant


class Command(BaseCommand):
    """Base command for use by actual commands."""

    @property
    def valiant(self) -> Valiant:
        """Access the Valiant application object."""
        return self.application.valiant  # noqa: DAR201
