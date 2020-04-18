"""CLI Command: show.

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
from valiant.package import PackageMetadata

from .package_command import PackageCommand, Payload


class ShowCommand(PackageCommand):
    """Describes a package.

    show
        {package : The package name}
        {version : The package version}
        {--r|repository= : The repository to use}
    """

    def prepare_data(self) -> Payload:
        """Gets the package metadata.

        Returns:
            Package metadata

        Raises:
            ValueError: When the package data can't be loaded
        """
        result = self.valiant.get_package_metadata(
            package_name=self.argument("package"),
            package_version=self.argument("version"),
            repository_name=self.option("repository"),
        )

        if not result:
            raise ValueError("Package details could not be loaded.")

        return Payload(metadata=result.package_metadata)

    def to_text(self, data: Payload) -> str:
        """Prepares text representations.

        Args:
            data: A payload that must have the package metadata.

        Returns:
            A nice bit of information to enhance your terminal.

        Raises:
            ValueError: If the payload is missing the package metadata.
        """
        if not data.metadata:
            raise ValueError("No package metadata available.")

        metadata: PackageMetadata = data.metadata
        return f"""\
<info>{metadata.name}:{metadata.version}</info>
<comment>Repository: <link>{metadata.repository_url}</link></comment>
<comment>Summary: {metadata.summary}</comment>"""
