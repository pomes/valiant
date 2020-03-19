"""CLI Command: show."""
from .command import Command


class ShowCommand(Command):
    """Describes a package.

    show
        {package : The package name}
        {version : The package version}
    """

    def handle(self) -> None:  # noqa: D102
        self.line(
            f"""\
<info>{self.argument("package")}:{self.argument("version")}</info>
"""
        )
