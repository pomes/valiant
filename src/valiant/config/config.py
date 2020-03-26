"""Configuration for Valiant."""
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Optional

from valiant.repositories import RepositoryConfiguration
from valiant.repositories.pypi import PyPiRepository
from valiant.reports import ReportProviderConfiguration


class Config:
    """Configuration object."""

    def __init__(
        self,
        repository_configurations: List[RepositoryConfiguration],
        config_dir: str,
        cache_dir: str,
        default_repository: Optional[str] = None,
        report_configuration: Optional[Dict[str, ReportProviderConfiguration]] = None,
    ):
        """Constructor.

        Args:
            repository_configurations: A list of repository configurations.
            cache_dir: Used by Valiant to cache assets.
            config_dir: Contains the configuration files.
            default_repository: The repository configuration to use by default
                                Only needed if there are > 1 repositories
            report_configuration: The report types to run by default

        Raises:
            ValueError: When the `repositories` list has items with the same name.
        """
        if len(repository_configurations) == 0:
            raise ValueError("No repositories were provided.")
        elif not default_repository and len(repository_configurations) > 1:
            raise ValueError("A default repository is required.")

        self._cache_dir = Path(cache_dir)
        self._config_dir = Path(config_dir)

        self._report_configuration: Optional[
            Dict[str, ReportProviderConfiguration]
        ] = None
        if report_configuration:
            self._report_configuration = deepcopy(report_configuration)

        self._repositories: Dict[str, RepositoryConfiguration] = {}

        for repo in repository_configurations:
            if repo.name in self._repositories:
                raise ValueError(f"Found repositories with the same name: {repo.name}")
            else:
                self._repositories[repo.name] = deepcopy(repo)

        if len(self._repositories) == 1 and not default_repository:
            self._default_repository = next(iter(self._repositories.keys()))
        elif default_repository:
            self._default_repository = default_repository
        else:  # pragma: no cover
            raise ValueError("Could not reconcile repository configuration.")

        if self._default_repository not in self._repositories:
            raise ValueError(
                f"The default repository ({self._default_repository})"
                " was not provided in the list of repositories."
            )

    @property
    def cache_dir(self) -> Path:
        """Path to the cache."""
        return self._cache_dir  # noqa: DAR201

    @property
    def config_dir(self) -> Path:
        """Path to the config dir."""
        return self._config_dir  # noqa: DAR201

    @property
    def report_configuration(self) -> Optional[Dict[str, ReportProviderConfiguration]]:
        """The reporting config."""
        return self._report_configuration  # noqa: DAR201

    @property
    def default_repository_name(self) -> str:
        """The default repo name."""
        return self._default_repository  # noqa: DAR201

    @property
    def default_repository_configuration(self) -> RepositoryConfiguration:
        """The default repo.

        Returns:
            If only one repository is listed then it is returned.
            Otherwise, the repository designated as the default_repository is returned.
        """
        return self.get_repository_configuration(self.default_repository_name)

    @property
    def repository_configuration(self) -> Dict[str, RepositoryConfiguration]:
        """All the repos.

        Returns:
            The job lot of repo configurations.
        """
        return self._repositories

    @property
    def repository_names(self) -> List[str]:
        """Returns a list of the known repositories.

        Use the names to call `get_repository`.

        Returns:
            A list of repository names.
        """
        return list(self._repositories.keys())

    def get_repository_configuration(self, key: str) -> RepositoryConfiguration:
        """Lookup a repository.

        Args:
            key: The name of the repository

        Returns:
            The repository configuration

        Raises:
            KeyError: If the name can't be found.
        """
        try:
            repo = self._repositories[key]
        except KeyError as ke:
            raise KeyError(f"Repository with name {key} could not be found.") from ke

        return repo


def _load_default_config() -> Config:
    """Returns an instance with the defaults.

    Returns:
        A default Config instance.
    """
    from appdirs import AppDirs

    from valiant.__about__ import (
        application_name,
        application_vendor,
        application_version,
    )

    dirs = AppDirs(
        appname=application_name,
        appauthor=application_vendor,
        version=application_version,
    )
    return Config(
        repository_configurations=[PyPiRepository.get_pypi_config()],
        config_dir=dirs.user_config_dir,
        cache_dir=dirs.user_cache_dir,
        report_configuration={
            "basic": ReportProviderConfiguration(),
            "spdx": ReportProviderConfiguration(),
            "safety": ReportProviderConfiguration(),
        },
    )
