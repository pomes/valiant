"""CLI Application config."""
from cleo.config import ApplicationConfig as BaseApplicationConfig  # pragma: no cover
from clikit.api.formatter import Style  # pragma: no cover


class ApplicationConfig(BaseApplicationConfig):  # pragma: no cover
    """Configures the CLI application."""

    _STYLES = [
        Style("c1").fg("cyan"),
        Style("info").fg("blue"),
        Style("comment").fg("green"),
        Style("error").fg("red").bold(),
        Style("warning").fg("yellow"),
        Style("debug").fg("black").bold(),
        Style("link").fg("blue").underlined(),
        Style("h1").fg("blue").bold().underlined(),
        Style("h2").fg("blue").underlined(),
    ]

    def configure(self) -> None:  # noqa: D102
        super(ApplicationConfig, self).configure()

        for style in ApplicationConfig._STYLES:
            self.add_style(style)
