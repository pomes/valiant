from cleo.config import ApplicationConfig as BaseApplicationConfig
from clikit.api.formatter import Style


class ApplicationConfig(BaseApplicationConfig):
    _STYLES = [
        Style("c1").fg("cyan"),
        Style("info").fg("blue"),
        Style("comment").fg("green"),
        Style("error").fg("red").bold(),
        Style("warning").fg("yellow"),
        Style("debug").fg("black").bold(),
    ]

    def configure(self):
        super(ApplicationConfig, self).configure()

        for style in ApplicationConfig._STYLES:
            self.add_style(style)
