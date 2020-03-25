"""Valiant CLI client."""
from cleo import Application as BaseApplication
from valiant import Factory, Valiant

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
        self._valiant: Valiant = Factory().create_valiant()
        super(Cli, self).__init__(
            name=self._valiant.application_name,
            version=self._valiant.application_version,
            config=ApplicationConfig(
                self._valiant.application_name, self._valiant.application_version,
            ),
        )
        self.add_commands(
            AboutCommand(),
            ConfigCommand(),
            AuditCommand(),
            ReportCommand(),
            ShowCommand(),
        )

    @property
    def valiant(self) -> Valiant:
        """Access the Valiant instance."""
        return self._valiant  # noqa: DAR201


if __name__ == "__main__":
    Cli().run()
