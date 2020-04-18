"""CLI Application config.

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
from cleo.config import ApplicationConfig as BaseApplicationConfig  # pragma: no cover
from clikit.api.args.format.option import Option
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

        self.add_option(
            "config",
            "c",
            Option.REQUIRED_VALUE | Option.STRING,
            "Load configuration from a TOML file",
        )

        self.add_option(
            "out",
            "o",
            Option.REQUIRED_VALUE | Option.STRING,
            "the desired output type (json, toml)",
        )
