"""Handles the valiant context.

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
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional, Set, Tuple

from valiant.config import Config
from valiant.package import PackageMetadata
from valiant.plugins.reports import ReportPlugins
from valiant.reports import ReportSet
from valiant.repositories import RepositoryConfiguration

from .__about__ import (
    application_copyright_holder,
    application_copyright_year,
    application_description,
    application_homepage,
    application_licence,
    application_name,
    application_tagline,
    application_title,
    application_vendor,
    application_version,
)


@dataclass(frozen=True)
class PythonPackagePayload:
    """A payload that collects package information."""

    repository_base_url: str
    package_name: str
    package_version: str
    package_metadata: PackageMetadata
    reports: Optional[ReportSet] = None

    def clone_with_reports(self, reports: ReportSet) -> "PythonPackagePayload":
        """Creates a new instance with a new report set.

        Args:
            reports: The new report set

        Returns:
            The new instance
        """
        import dataclasses

        return dataclasses.replace(
            self,
            repository_base_url=self.repository_base_url,
            package_name=self.package_name,
            package_version=self.package_version,
            package_metadata=self.package_metadata,
            reports=reports,
        )


class Valiant:
    """Provides general applications details and instance configuration."""

    def __init__(self, config: Config):
        """Fire up a new valiant.

        Args:
            config: The application configuration
        """
        from valiant.repositories import RepositoryFactory

        self._config: Config = config
        self._repo_factory = RepositoryFactory()

        local_plugins: Optional[Mapping[str, str]] = None
        if self._config.local_report_plugins:
            local_plugins = self._config.local_report_plugins

        self._report_plugins: ReportPlugins = ReportPlugins(local_plugins=local_plugins)
        self._report_plugins.load_plugins()

    @staticmethod
    def application_details() -> Tuple:  # noqa: D102
        return (application_vendor, application_name, application_version)

    @property
    def application_version(self) -> str:  # noqa: D102
        return application_version

    @property
    def application_name(self) -> str:  # noqa: D102
        return application_name

    @property
    def application_vendor(self) -> str:  # noqa: D102
        return application_vendor

    @property
    def application_title(self) -> str:  # noqa: D102
        return application_title

    @property
    def application_description(self) -> str:  # noqa: D102
        return application_description

    @property
    def application_tagline(self) -> str:  # noqa: D102
        return application_tagline

    @property
    def application_licence(self) -> str:  # noqa: D102
        return application_licence

    @property
    def application_homepage(self) -> str:  # noqa: D102
        return application_homepage

    @property
    def application_copyright_year(self) -> int:  # noqa: D102
        return application_copyright_year

    @property
    def application_copyright_holder(self) -> str:  # noqa: D102
        return application_copyright_holder

    def configuration_to_json(self) -> str:  # noqa: D102
        return self._config.to_json()

    def configuration_to_toml(self) -> str:  # noqa: D102
        return self._config.to_toml()

    @property
    def cache_dir(self) -> Optional[Path]:
        """Gets the current instance's cache dir.

        Returns:
            A Path object to the cache directory
        """
        return self._config.cache_dir

    @property
    def configuration_dir(self) -> Optional[Path]:
        """Gets the current instance's config dir.

        Returns:
            A Path object to the config directory
        """
        return self._config.configuration_dir

    @property
    def log_dir(self) -> Optional[Path]:
        """Gets the current instance's log dir.

        Returns:
            A Path object to the config directory
        """
        return self._config.log_dir

    @property
    def default_reports(self) -> Set[str]:
        """Get a set of the default reports.

        Returns:
            A set of report names
        """
        return self._config.default_reports

    @property
    def default_repository_name(self) -> str:
        """The default repo name."""
        return self._config.default_repository_name  # noqa: DAR201

    @property
    def repository_configuration(self) -> Mapping[str, RepositoryConfiguration]:
        """All the repos.

        Returns:
            The job lot of repo configurations.
        """
        return self._config.repository_configurations

    @property
    def loaded_report_plugin_names(self) -> Set[str]:
        """Returns the set of loaded reporting plugins."""
        if self._report_plugins.names:  # noqa: DAR201
            return set(self._report_plugins.names)
        return set()

    @property
    def loaded_report_plugins(self) -> Set[Tuple[str, str]]:
        """Returns a set of name,version tuples for the loaded plugins."""
        if self._report_plugins:  # noqa: DAR201
            return set(
                [
                    (p.plugin_name, p.plugin_version)
                    for p in self._report_plugins.plugins.values()
                ]
            )

        return set()

    def get_package_metadata(
        self,
        package_name: str,
        package_version: str,
        repository_name: Optional[str] = None,
    ) -> PythonPackagePayload:
        """Gets the metadata for the requested package.

        Args:
            package_name: The package name
            package_version: The package version
            repository_name: The name(key) for the repository to use

        Returns:
            A payload with the package metadata.
        """
        if repository_name:
            repo_config = self._config.get_repository_configuration(repository_name)
        else:
            repo_config = self._config.default_repository_configuration

        repo = self._repo_factory.get_repository(repo_config)

        metadata = repo.show(package_name, package_version)

        return PythonPackagePayload(
            repository_base_url=repo_config.base_url,
            package_name=package_name,
            package_version=package_version,
            package_metadata=metadata,
        )

    def get_package_reports(
        self, payload: PythonPackagePayload, reports: Set[str] = None
    ) -> PythonPackagePayload:
        """Prepares the reports for the package defined in the payload.

        Args:
            payload: A payload generated by `get_package_metadata`
            reports: A list of the specific reports to run.
                     If no list is provided, all the configured reports are run.

        Returns:
            A new payload instance enhanced with reports.

        Raises:
            ValueError: If any of the requested reports aren't available in the list
                        of loaded report plugins.
        """
        report_list = set(reports or self._config.default_reports)

        if not report_list.issubset(self.loaded_report_plugin_names):
            raise ValueError(
                f"The requested reports ({report_list}) is not a subset "
                f"of the loaded report plugins ({self.loaded_report_plugin_names})"
            )

        report_set = ReportSet()
        for report in report_list:
            report_plugin = self._report_plugins.get(report)
            if not report_plugin:
                raise ValueError("")

            report_set.add_report(
                report_plugin.run(
                    configuration_dir=self.configuration_dir,
                    package_metadata=payload.package_metadata,
                )
            )

        return payload.clone_with_reports(report_set)
