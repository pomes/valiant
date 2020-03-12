from cleo import Application as BaseApplication
from valiant import Valiant, factory

from .commands.about import AboutCommand
from .commands.config import ConfigCommand
from .commands.search import SearchCommand
from .commands.show import ShowCommand
from .config import ApplicationConfig


class Cli(BaseApplication):
    def __init__(self):
        super(Cli, self).__init__(
            Valiant.application_name(),
            Valiant.application_version(),
            config=ApplicationConfig(
                Valiant.application_name(), Valiant.application_version()
            ),
        )
        self._valiant: Valiant = factory()
        self.add_commands(
            AboutCommand(), ConfigCommand(), SearchCommand(), ShowCommand()
        )

    @property
    def valiant(self) -> Valiant:
        return self._valiant


if __name__ == "__main__":
    Cli().run()
