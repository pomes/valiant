"""CLI Command: show."""
from typing import Any, Dict

from .command import Command


class ShowCommand(Command):
    """Describes a package.

    show
        {package : The package name}
        {version : The package version}
        {--r|repository= : The repository to use}
        {--o|out= : the desired output type (json)}
    """

    def prepare_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Gets the package metadata.

        Args:
            kwargs: Not used

        Returns:
            Package metadata

        Raises:
            ValueError: When the package data can't be loaded
        """  # noqa:DAR101,DAR201
        result = self.valiant.get_package_metadata(
            package_name=self.argument("package"),
            package_version=self.argument("version"),
            repository_name=self.option("repository"),
        )

        if not result:
            raise ValueError("Package details could not be loaded.")

        return {
            "repo_url": result.repository_base_url,
            "metadata": result.package_metadata.to_dict(),
        }

    def to_text(self, data: Dict[str, Any]) -> str:
        """Prepares text representations."""  # noqa:DAR101,DAR201
        return f"""\
<info>{data["metadata"]["name"]}:{data["metadata"]["version"]}</info>
<comment>Repository: <link>{data["repo_url"]}</link></comment>
<comment>Summary: {data["metadata"]["summary"]}</comment>"""
