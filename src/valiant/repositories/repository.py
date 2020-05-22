"""Base class for Python repos.

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
                "Unable to handle repositories of type "
                f"{repository_configuration.repository_type}."
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
