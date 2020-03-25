"""CLI Command: show."""
from valiant.package import PackageMetadata

from .package_command import PackageCommand, Payload


class ShowCommand(PackageCommand):
    """Describes a package.

    show
        {package : The package name}
        {version : The package version}
        {--r|repository= : The repository to use}
        {--o|out= : the desired output type (json)}
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
