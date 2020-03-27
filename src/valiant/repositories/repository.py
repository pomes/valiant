"""Base class for Python repos."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from ..package import PackageMetadata
from .config import RepositoryConfiguration


class BaseRepository(ABC):
    """Interface definition for repo functionality."""

    def __init__(
        self, repository_configuration: RepositoryConfiguration,
    ):
        """New instance.

        The repository_config argument trumps the base_url argument.

        Args:
            repository_configuration: A RepositoryConfiguration instance

        Raises:
            ValueError: If no configuration is provided or
                        no handler is available for the repo type.
        """
        if (
            repository_configuration.repository_type
            not in self.__class__.list_supported_repository_types()
        ):
            raise ValueError(
                f"Unable to handle repositories of type "
                "repository_configuration.repository_type}."
            )

        self._config = repository_configuration

    @property
    def repository_configuration(self) -> RepositoryConfiguration:
        """Get the config."""
        return self._config  # noqa: DAR201

    @property
    def repository_type(self) -> str:
        """Identifies the underlying software supported by the repo.

        Returns:
            The repo type.
        """
        return self._config.repository_type

    @classmethod
    def list_supported_repository_types(cls) -> List[str]:
        """Lists the repository types support by this implementation."""
        return []  # noqa: DAR201

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
