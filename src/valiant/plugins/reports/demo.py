"""Demonstrator plugin.

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
from pathlib import Path

from valiant.plugins.reports import (
    BaseReportPlugin,
    Finding,
    FindingCategory,
    FindingLevel,
    PackageMetadata,
    Report,
    get_logger,
)

log = get_logger()


class DemoReportPlugin(BaseReportPlugin):
    """A sample reporting plugin."""

    name = "demo"
    vendor = "Valiant"
    display_name = "Demo"
    version = "0.1"
    url = ""

    @classmethod
    def prepare_report(
        cls, package_metadata: PackageMetadata, configuration_dir: Path
    ) -> Report:
        """Run the report.

        Args:
            package_metadata: The package information
            configuration_dir: A directory for locating config

        Returns:
            A report with (perhaps) a finding or two.
        """
        report = Report(cls.report_provider_details())
        log.info(
            "The demo plugin was called",
            package_name=package_metadata.name,
            package_version=package_metadata.version,
        )
        report.add_finding(
            Finding(
                coordinates=package_metadata.coordinates,
                id="DEMO001",
                title="Demo finding",
                category=FindingCategory.PROJECT.value,
                level=FindingLevel.INFO,
                message="This is a demo finding",
                data={"value": "demo"},
                url="http://www.example.com",
            )
        )
        return report
