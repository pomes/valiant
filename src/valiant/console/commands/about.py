"""CLI Command: about."""
import json

from typing import Dict, Optional

import toml

from .base_command import BaseCommand


class AboutCommand(BaseCommand):
    """Shows information about Valiant.

    about
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

    def to_dict(self) -> Dict:  # noqa: D102
        return {
            "name": self.valiant.application_name,
            "version": self.valiant.application_version,
            "license": self.valiant.application_licence,
            "url": self.valiant.application_homepage,
        }

    def to_json(self) -> str:  # noqa: D102
        return json.dumps(self.to_dict())

    def to_toml(self) -> str:  # noqa: D102
        return toml.dumps(
            {"tool": {self.valiant.application_name: {"about": self.to_dict()}}}
        )

    def to_text(self) -> str:  # noqa: D102
        return f"""\
<info>{self.valiant.application_title} {self.valiant.application_version}</info>
<comment>- {self.valiant.application_tagline} - </comment>

<comment>{self.valiant.application_description}</comment>

<comment>Licence: {self.valiant.application_licence}</comment>
<comment>See <link>{self.valiant.application_homepage}</link> for more information.</comment>"""
