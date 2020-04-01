"""Handles the valiant context."""
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional, Set, Tuple

from valiant.config import Config
from valiant.package import PackageMetadata
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
        from valiant.reports import ReportFactory
        from valiant.repositories import RepositoryFactory

        self._config: Config = config
        self._repo_factory = RepositoryFactory()
        self._report_factory = ReportFactory()

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
        """
        if not reports or len(reports) == 0:
            report_set = self._report_factory.generate_reports(
                package_metadata=payload.package_metadata,
                report_list=self._config.default_reports,
            )
        else:
            report_set = self._report_factory.generate_reports(
                package_metadata=payload.package_metadata, report_list=reports,
            )

        return payload.clone_with_reports(report_set)
