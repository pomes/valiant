"""CLI Command: about."""
import json
from typing import Optional
from .base_command import BaseCommand


class AboutCommand(BaseCommand):
    """Shows information about Valiant.

    about
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
                "application": {
                    "name": self.valiant.application_name,
                    "version": self.valiant.application_version,
                    "license": self.valiant.application_licence,
                    "url": self.valiant.application_homepage,
                }
            }
        )

    def to_text(self) -> str:  # noqa: D102
        return f"""\
<info>{self.valiant.application_title} {self.valiant.application_version}</info>
<comment>- {self.valiant.application_tagline} - </comment>

<comment>{self.valiant.application_description}</comment>

<comment>Licence: {self.valiant.application_licence}</comment>
<comment>See <link>{self.valiant.application_homepage}</link> for more information.</comment>"""
