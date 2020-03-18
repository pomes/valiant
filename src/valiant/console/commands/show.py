"""CLI Command: show."""
from .command import Command


class ShowCommand(Command):
    """Describes a package.

    show
        {package : The package name}
    """

    def handle(self) -> None:  # noqa: D102
        pass
