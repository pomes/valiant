"""Configuration for Valiant.

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
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path

from typing import Any, Dict, List, Mapping, Optional, Set, Tuple, Union

from valiant.repositories import RepositoryConfiguration
from valiant.util import Dictionizer


@dataclass(frozen=True)
class Config(Dictionizer):
    """Configuration object."""

    configuration_dir: Path
    cache_dir: Path
    log_dir: Path
    default_repository: str
    repository_configurations: Mapping[str, RepositoryConfiguration]
    default_reports: Set[str]
    requests_cache: Mapping[str, Union[str, int]]
    logging_configuration: Mapping
    logging_configuration_file: Optional[Path]
    local_plugin_paths: List[str] = field(default_factory=list)
    local_report_plugins: Mapping[str, str] = field(default_factory=dict)
    metadata: Optional[Mapping[str, Any]] = None

    def __post_init__(self):
        """Performs post init checks.

        Raises:
            ValueError: if the config isn't meeting the mark
        """
        import sys
        from string import Template
        from requests_cache import install_cache
        from valiant.log import configure_logging

        if self.default_repository not in self.repository_configurations.keys():
            raise ValueError(
                f"The default repository ({self.default_repository})"
                " was not provided in the list of repositories."
            )

        sys.path.extend(self.local_plugin_paths)

        # Make sure the required directories exist
        self.configuration_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        if not self.logging_configuration_file:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            # Manipulate the log file location for the built-in logging definition
            log_file_t = Template(
                self.logging_configuration["handlers"]["default"]["filename"]
            )
            self.logging_configuration["handlers"]["default"][
                "filename"
            ] = log_file_t.substitute(
                log_dir=self.log_dir,
                cache_dir=self.cache_dir,
                configuration_dir=self.configuration_dir,
            )

        configure_logging(
            dict_config=self.logging_configuration,
            file_config=self.logging_configuration_file,
        )

        rcache_dir = Template(self.requests_cache["file"])

        install_cache(
            rcache_dir.substitute(
                log_dir=self.log_dir,
                cache_dir=self.cache_dir,
                configuration_dir=self.configuration_dir,
            ),
            backend=self.requests_cache["backend"],
            expire_after=self.requests_cache["expire_after"],
        )

    def to_dict(self) -> Dict:
        """Convert to dict.

        Note that only a subset of the configuration items are currently
        returned to reflect those items for which configuration is
        supported.

        Returns:
            A subset of the configuration.
        """
        return {
            "tool": {
                "valiant": {
                    "configuration_dir": str(self.configuration_dir),
                    "cache_dir": str(self.cache_dir),
                    "log_dir": str(self.log_dir),
                    "default_repository": self.default_repository,
                    "repository_configurations": {
                        k: self.repository_configurations[k].to_dict()
                        for k in self.repository_configurations.keys()
                    },
                    "default_reports": list(self.default_reports),
                    "logging_configuration_file": str(self.logging_configuration_file)
                    if self.logging_configuration_file
                    else None,
                    "requests_cache": self.requests_cache,
                    "local-plugins": {
                        "paths": [str(i) for i in self.local_plugin_paths],
                        "valiant.report": self.local_report_plugins,
                    },
                }
            }
        }

    @staticmethod
    def prepare_repository_configurations(
        repository_configurations: List[RepositoryConfiguration],
        default_repository: str = None,
    ) -> Tuple[str, Dict[str, RepositoryConfiguration]]:
        """Helper method to setup repository_configurations.

        Primarily maps the config list to a dict using the repo name as the key.
        If no default_repository is nominated and the list has only 1 member then
        that repo is set to be the default.

        Args:
            repository_configurations: A list of repo configs
            default_repository: A nominated default

        Returns:
            A tuple of (default_repository, repository_configurations)

        Raises:
            ValueError: if multiple repo configs have the same name,
                or a default_repo could not be determined,
                or a default_repo is set but doesn't exist as a key in the resulting map.
        """
        repositories: Dict[str, RepositoryConfiguration] = {}

        for repo in repository_configurations:
            if repo.name in repositories:
                raise ValueError(f"Found repositories with the same name: {repo.name}")
            else:
                repositories[repo.name] = deepcopy(repo)

        if len(repositories) == 1 and not default_repository:
            def_repo = next(iter(repositories.keys()))
        elif default_repository:
            def_repo = default_repository
        else:  # pragma: no cover
            raise ValueError("Could not reconcile repository configuration.")

        if def_repo not in repositories:
            raise ValueError(
                f"The default repository ({def_repo})"
                " was not provided in the list of repositories."
            )

        return def_repo, repositories

    @property
    def default_repository_name(self) -> str:
        """The default repo name."""
        return self.default_repository  # noqa: DAR201

    @property
    def default_repository_configuration(self) -> RepositoryConfiguration:
        """The default repo.

        Returns:
            If only one repository is listed then it is returned.
            Otherwise, the repository designated as the default_repository is returned.
        """
        return self.get_repository_configuration(self.default_repository_name)

    @property
    def repository_names(self) -> List[str]:
        """Returns a list of the known repositories.

        Use the names to call `get_repository`.

        Returns:
            A list of repository names.
        """
        return list(self.repository_configurations.keys())

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
            repo = self.repository_configurations[key]
        except KeyError as ke:
            raise KeyError(f"Repository with name {key} could not be found.") from ke

        return repo
