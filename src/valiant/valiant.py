"""Handles the valiant context."""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from requests_cache import install_cache
from valiant.log import configure_logging, setup_logging_configuration
from valiant.repositories import RepositoryFactory

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
from .config import Config
from .package import PackageMetadata
from .reports import ReportFactory, ReportProviderConfiguration, ReportSet
from valiant.repositories import RepositoryConfiguration


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
        return PythonPackagePayload(
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
        self._config: Config = config
        self._repo_factory = RepositoryFactory()
        self._report_factory = ReportFactory()

        # Make sure the required directories exist
        self._config.config_dir.mkdir(parents=True, exist_ok=True)
        self._config.cache_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        log_config = setup_logging_configuration(
            handlers={
                "default": {
                    "level": "INFO",
                    "formatter": "standard",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": Path(self._config.config_dir, "valiant.log"),
                    "maxBytes": 500000,
                    "backupCount": 3,
                }
            },
        )
        configure_logging(log_config)

        # TODO: this is just basic caching for now
        install_cache(
            f"{application_name}-{application_version}-requests-cache",
            backend="sqlite",
            expire_after=86400,
        )

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

    @property
    def cache_dir(self) -> Optional[Path]:
        """Gets the current instance's cache dir.

        Returns:
            A Path object to the cache directory
        """
        return self._config.cache_dir

    @property
    def config_dir(self) -> Optional[Path]:
        """Gets the current instance's config dir.

        Returns:
            A Path object to the config directory
        """
        return self._config.config_dir

    @property
    def default_repository_name(self) -> str:
        """The default repo name."""
        return self._config.default_repository_name  # noqa: DAR201

    @property
    def repository_configuration(self) -> Dict[str, RepositoryConfiguration]:
        """All the repos.

        Returns:
            The job lot of repo configurations.
        """
        return self._config.repository_configuration

    @property
    def report_configuration(self) -> Dict[str, ReportProviderConfiguration]:
        """The reporting config.

        Returns:
            A dict of the config. Can be empty.
        """
        if not self._config.report_configuration:
            return {}
        return self._config.report_configuration

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
        self, payload: PythonPackagePayload, reports: List[str] = None
    ) -> PythonPackagePayload:
        """Prepares the reports for the package defined in the payload.

        Args:
            payload: A payload generated by `get_package_metadata`
            reports: A list of the specific reports to run.
                     If no list is provided, all the configured reports are run.

        Returns:
            A new payload instance enhanced with reports.

        Raises:
            ValueError: When no report config is provided.
        """
        if not self._config.report_configuration:
            raise ValueError("No report configuration has been provided.")

        if not reports or len(reports) == 0:
            report_set = self._report_factory.generate_reports(
                package_metadata=payload.package_metadata,
                configuration=self._config.report_configuration,
            )
        else:
            report_configuration: Dict[str, ReportProviderConfiguration] = {}
            for item in reports:
                report_configuration[item] = self._config.report_configuration[item]

            report_set = self._report_factory.generate_reports(
                package_metadata=payload.package_metadata,
                configuration=report_configuration,
            )

        return payload.clone_with_reports(report_set)
