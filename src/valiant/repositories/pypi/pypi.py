"""The much adored central Python repo."""

import sys

from pathlib import Path
from typing import Any, Dict

import requests

from .. import BaseRepository, PackageNotFoundException, RepositoryException
from . import PyPiPackageMetadata


class PyPiRepository(BaseRepository):
    """The central Python repository.

    This class may also work on servers also running the Warehouse system.

    See: https://warehouse.readthedocs.io/api-reference/json/
    """

    def __init__(self, base_url: str = "https://pypi.org/pypi"):
        """New instance.

        Args:
            base_url: The base API url for the repository
        """
        self._base_url: str = base_url

    @property
    def base_url(self) -> str:  # noqa: D102
        return self._base_url

    def _load_package_manifest(self, name: str, version: str) -> Dict[Any, Any]:
        """Downloads the JSON metadata from the repository.

        Args:
            name: The package name.
            version: The package version.

        Returns:
            The JSON-based metadata (as a string).

        Raises:
            PackageNotFoundException: When the URL doesn't work.
            RepositoryException: If the JSON data is empty(None)
        """
        url = f"{self._base_url}/{name}/{version}/json"

        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            raise PackageNotFoundException(f"No result for {url}")

        data = r.json()

        if data is None:
            raise RepositoryException("The JSON response was empty.")

        return data

    def show(self, name: str, version: str) -> PyPiPackageMetadata:
        """Provides details for a specific package version.

        Args:
            name: The package name
            version: The package version

        Returns:
            A package instance if it can be located. None otherwise.

        Raises:
            PackageNotFoundException: When the package cannot be found
            ValidationError: The package metadata could not be parsed. # noqa: DAR402
        """
        try:
            data = self._load_package_manifest(name, version)
        except (PackageNotFoundException, RepositoryException) as e:
            raise PackageNotFoundException(f"Failed to access package metadata: {e}")

        return PyPiPackageMetadata(data)

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


if __name__ == "__main__":
    """Just a small cli.

    Sample call:
        poetry run python -m valiant.repositories.pypi.pypi flask 1.1.1
    """

    if len(sys.argv) == 3:
        repo = PyPiRepository()
        pkg = repo.show(name=sys.argv[1], version=sys.argv[2])

        print(f"{pkg}")
    else:
        print("Usage: pypi <package> <version>")