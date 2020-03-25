"""CLI Command: config."""
import json
from typing import Optional
from .base_command import BaseCommand


class ConfigCommand(BaseCommand):
    """Application configuration.

    config
        {--o|out= : the desired output type (json)}
    """

    def handle(self) -> Optional[int]:  # noqa: D102
        format = self.option("out")
        if format == "json":
            self.line(self.to_json())
        else:
            self.line(self.to_text())
        return 0

    def to_json(self) -> str:  # noqa: D102
        return json.dumps(
            {
                "cache_dir": str(self.valiant.cache_dir),
                "config_dir": str(self.valiant.config_dir),
                "default_repository_name": self.valiant.default_repository_name,
                "repositories": {
                    k: v.to_dict()
                    for k, v in self.valiant.repository_configuration.items()
                },
                "reports": {
                    k: v.items for k, v in self.valiant.report_configuration.items()
                },
            }
        )

    def to_text(self) -> str:  # noqa: D102
        repo_config = ",".join(self.valiant.repository_configuration.keys())
        report_config = ",".join(self.valiant.report_configuration.keys())
        return f"""\
<info>cache_dir</info>: <comment>{self.valiant.cache_dir}</comment>
<info>config_dir</info>: <comment>{self.valiant.config_dir}</comment>
<info>default_repository_name</info>: <comment>{self.valiant.default_repository_name}</comment>
<info>repositories</info>: <comment>{repo_config}</comment>
<info>reports</info>: <comment>{report_config}</comment>"""
