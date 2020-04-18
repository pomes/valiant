"""Works out which repo wrangler ya need.

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
from .config import RepositoryConfiguration
from .repository import BaseRepository


class RepositoryFactory:
    """Helps construct a repository instance based on the configuration."""

    def __init__(self):
        """Constructor."""
        from typing import Dict

        self._cache: Dict[str, BaseRepository] = {}

    def _instantiate_handler(self, conf: RepositoryConfiguration) -> BaseRepository:
        from .pypi import PyPiRepository

        if conf.repository_type in PyPiRepository.list_supported_repository_types():
            return PyPiRepository(conf)

        raise ValueError(
            f"Unable to handle repositories of type {conf.repository_type}"
        )

    def _check_cache(self, conf: RepositoryConfiguration) -> BaseRepository:
        if conf.name in self._cache:
            if self._cache[conf.name].repository_configuration != conf:
                raise ValueError(
                    "Cache clash"
                    " - repository configuration uses the same name as an existing cache entry"
                )
        else:
            self._cache[conf.name] = self._instantiate_handler(conf)

        return self._cache[conf.name]

    def get_repository(
        self, repository_configuration: RepositoryConfiguration,
    ) -> BaseRepository:
        """Factory method.

        Args:
            repository_configuration: The repository config

        Returns:
            A repository instance that handles the type set in the config
        """
        return self._check_cache(repository_configuration)

    def reset_cache(self) -> None:
        """Clears the cache."""
        self._cache = {}
