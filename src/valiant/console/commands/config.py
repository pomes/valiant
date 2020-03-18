"""Configuration command."""
from .command import Command


class ConfigCommand(Command):
    """Lists the configuration settings.

    config
    """

    def handle(self) -> None:  # noqa: D102
        self.line(f"""<info>cache-dir</info> = {self.valiant.cache_dir}""")
