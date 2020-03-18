"""Base class for Python repos."""

from abc import ABC, abstractmethod
from pathlib import Path

from . import PackageMetadata


class BaseRepository(ABC):
    """Interface definition for repo functionality."""

    @abstractmethod
    def show(self, name: str, version: str) -> PackageMetadata:
        """Provides details for a specific package version.

        Args:
            name: The package name
            version: The package version

        # noqa: DAR202
        Returns:
            A package instance if it can be located.

        Raises:
            NotImplementedError: Because this is an abstract implementation.
            PackageNotFoundException: When the package cannot be found. # noqa: DAR402
            ValidationError: The package metadata could not be parsed. # noqa: DAR402
        """
        raise NotImplementedError

    @abstractmethod
    def download(self, name: str, version: str) -> Path:
        """Provides details for a specific package version.

        Args:
            name: The package name
            version: The package version

        # noqa: DAR202
        Returns:
            The path to the download if the artifact can be located.

        Raises:
            NotImplementedError: Because this is an abstract implementation.
        """
        raise NotImplementedError
