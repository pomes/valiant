"""CLI Command: config."""
from typing import Optional
from .base_command import BaseCommand


class ConfigCommand(BaseCommand):
    """Application configuration.

    config
    """

    def handle(self) -> Optional[int]:  # noqa: D102
        format = self.option("out")
        if format == "json":
            self.line(self.to_json())
        elif format == "toml":
            self.line(self.to_toml())
        else:
            self.line(self.to_text())
        return 0

    def to_json(self) -> str:  # noqa: D102
        return self.valiant.configuration_to_json()

    def to_toml(self) -> str:  # noqa: D102
        return self.valiant.configuration_to_toml()

    def to_text(self) -> str:  # noqa: D102

        repo_config = ",".join(self.valiant.repository_configuration.keys())

        verbose_text = ""
        if self.io.is_verbose():
            from pprint import pformat

            verbose_text = (
                "\n<info>metadata:</info>\n  <comment>"
                + pformat(self.valiant._config.metadata, compact=True, sort_dicts=False)
                + "</comment>"
            )

        return (
            f"<info>configuration_dir</info>: "
            f"<comment>{self.valiant.configuration_dir}</comment>"
            f"\n<info>cache_dir</info>: <comment>{self.valiant.cache_dir}</comment>"
            f"\n<info>log_dir</info>: <comment>{self.valiant.log_dir}</comment>"
            f"\n<info>default_repository</info>: "
            f"<comment>{self.valiant.default_repository_name}</comment>"
            f"\n<info>repositories</info>: <comment>{repo_config}</comment>"
            f"\n<info>reports</info> : <comment> {self.valiant.default_reports} </comment>"
            f"{verbose_text}"
        )
