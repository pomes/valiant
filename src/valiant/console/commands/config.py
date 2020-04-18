"""CLI Command: config.

Copyright (c) 2020 The Valiant Authors

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
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

        if self.io.is_debug():
            from pprint import pformat

            verbose_text = (
                "\n<info>All config data:</info>\n  <comment>"
                + pformat(
                    self.valiant._config.to_dict(), compact=True, sort_dicts=False
                )
                + "</comment>"
            )
        elif self.io.is_verbose():
            from pprint import pformat

            verbose_text = (
                "\n<info>metadata:</info>\n  <comment>"
                + pformat(self.valiant._config.metadata, compact=True, sort_dicts=False)
                + "</comment>"
            )

        loaded_plugins = ", ".join(
            [f"{p[0]}:{p[1]}" for p in self.valiant.loaded_report_plugins]
        )

        return (
            "<info>configuration_dir</info>: "
            f"<comment>{self.valiant.configuration_dir}</comment>"
            f"\n<info>cache_dir</info>: <comment>{self.valiant.cache_dir}</comment>"
            f"\n<info>log_dir</info>: <comment>{self.valiant.log_dir}</comment>"
            "\n<info>logging_configuration_file</info>: "
            f"<comment>{self.valiant._config.logging_configuration_file}</comment>"
            f"\n<info>default_repository</info>: "
            f"<comment>{self.valiant.default_repository_name}</comment>"
            f"\n<info>repositories</info>: <comment>{repo_config}</comment>"
            f"\n<info>reports</info>: <comment> {self.valiant.default_reports} </comment>"
            "\n<info>Loaded report plugins</info>: "
            f"<comment>{loaded_plugins}</comment>"
            f"{verbose_text}"
        )
