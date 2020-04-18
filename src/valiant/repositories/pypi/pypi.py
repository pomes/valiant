"""The much adored central Python repo.

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
import sys

from pathlib import Path
from typing import Any, Dict, List

import requests

from valiant.log import get_logger
from valiant.repositories import (
    BaseRepository,
    PackageNotFoundException,
    RepositoryConfiguration,
    RepositoryException,
)
from .model import PyPiPackageMetadata

log = get_logger()


class PyPiRepository(BaseRepository):
    """The central Python repository.

    This class may also work on servers also running the Warehouse system.

    See: https://warehouse.readthedocs.io/api-reference/json/
    """

    @classmethod
    def list_supported_repository_types(cls) -> List[str]:
        """Lists the repository types support by this implementation."""
        return ["warehouse", "pypi"]  # noqa: DAR201

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
        url = f"{self.repository_configuration.get_access_url()}/{name}/{version}/json"

        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            log.error(
                "Package not found",
                package_name=name,
                package_version=version,
                repository_url=self.repository_configuration.base_url,
                status_code=r.status_code,
            )
            raise PackageNotFoundException(f"No result for {url}")

        if hasattr(r, "cache_used"):
            log.info(
                "Package found",
                package_name=name,
                package_version=version,
                repository_url=self.repository_configuration.base_url,
                cache_enabled=True,
                cache_used=r.cache_used,  # type: ignore
            )
        else:
            log.info(
                "Package found",
                package_name=name,
                package_version=version,
                repository_url=self.repository_configuration.base_url,
                cache_enabled=False,
                cache_used=False,
            )

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

        return PyPiPackageMetadata(
            repository_url=self.repository_configuration.base_url, package_data=data
        )

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

    @staticmethod
    def get_pypi_config() -> RepositoryConfiguration:
        """Helper for the central repo.

        Returns:
            A config for the PyPi repo
        """
        return RepositoryConfiguration(
            name="pypi", base_url="https://pypi.org/pypi", repository_type="warehouse"
        )


if __name__ == "__main__":
    """Just a small cli.

    Sample call:
        poetry run python -m valiant.repositories.pypi.pypi flask 1.1.1
    """

    if len(sys.argv) == 3:
        repo = PyPiRepository(PyPiRepository.get_pypi_config())
        pkg = repo.show(name=sys.argv[1], version=sys.argv[2])

        print(f"{pkg}")
    else:
        print("Usage: pypi <package> <version>")
