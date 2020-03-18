"""CLI Command: about."""
from .command import Command


class AboutCommand(Command):
    """Shows information about Valiant.

    about
    """

    def handle(self) -> None:  # noqa: D102

        self.line(
            f"""
<info>{self.valiant.application_title()} - {self.valiant.application_tagline()}</info>

<comment>Licence: {self.valiant.application_licence()}</comment>
<comment>{self.valiant.application_description()}.
See <fg=blue>{self.valiant.application_homepage()}</> for more information.</comment>
"""
        )
