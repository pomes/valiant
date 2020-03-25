"""CLI Command: about."""
from .command import Command, Payload


class AboutCommand(Command):
    """Shows information about Valiant.

    about
        {--o|out= : the desired output type (json)}
    """

    def prepare_data(self) -> Payload:
        """Preps the app data.

        Returns:
            A payload with the message describing the application.
        """
        msg = f"""\
<info>{self.valiant.application_title} {self.valiant.application_version}</info>
<comment>- {self.valiant.application_tagline} - </comment>

<comment>{self.valiant.application_description}</comment>

<comment>Licence: {self.valiant.application_licence}</comment>
<comment>See <link>{self.valiant.application_homepage}</link> for more information.</comment>"""
        return Payload(message=msg)
