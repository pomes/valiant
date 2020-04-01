"""Valiant CLI client."""
from cleo import Application as BaseApplication
from valiant import Valiant

from .commands import (
    AboutCommand,
    AuditCommand,
    ConfigCommand,
    ReportCommand,
    ShowCommand,
)
from .config import ApplicationConfig


class Cli(BaseApplication):
    """The CLI client app."""

    def __init__(self):
        """Constructor."""
        _, name, version = Valiant.application_details()
        super(Cli, self).__init__(
            name=name, version=version, config=ApplicationConfig(name, version),
        )

        self.add_commands(
            AboutCommand(),
            ConfigCommand(),
            AuditCommand(),
            ReportCommand(),
            ShowCommand(),
        )


if __name__ == "__main__":
    Cli().run()
