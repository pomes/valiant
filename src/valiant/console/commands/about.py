"""CLI Command: about."""
from typing import Any, Dict

from .command import Command


class AboutCommand(Command):
    """Shows information about Valiant.

    about
        {--o|out= : the desired output type (json)}
    """

    def prepare_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Preps the app data.

        Args:
            kwargs: Not used.

        Returns:
            App data
        """
        return {
            "name": self.valiant.application_name,
            "title": self.valiant.application_title,
            "version": self.valiant.application_version,
            "tagline": self.valiant.application_tagline,
            "licence": self.valiant.application_licence,
            "description": self.valiant.application_description,
            "homepage": self.valiant.application_homepage,
        }

    def to_text(self, data: Dict[str, Any]) -> str:  # noqa:DAR102
        return f"""\
<info>{data["title"]} {data["version"]} - {data["tagline"]}</info>

<comment>{data["description"]}</comment>

<comment>Licence: {data["licence"]}</comment>
<comment>See <link>{data["homepage"]}</link> for more information.</comment>"""
