"""CLI Command: about.

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
