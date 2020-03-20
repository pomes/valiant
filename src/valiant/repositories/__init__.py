"""Classes related to working with Python package repositories."""

from .config import RepositoryConfiguration
from .exceptions import PackageNotFoundException, RepositoryException, ValidationError
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
