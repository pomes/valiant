"""Handles the valiant context."""
from pathlib import Path

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
    default_config,
)
from .config import Config


class Valiant:
    """Provides general applications details and instance configuration."""

    def __init__(self, config: Config):
        """Fire up a new valiant.

        Args:
            config: The application configuration
        """
        self._config: Config = config

    @classmethod
    def application_version(cls) -> str:  # noqa
        return application_version

    @classmethod
    def application_name(cls) -> str:  # noqa
        return application_name

    @classmethod
    def application_vendor(cls) -> str:  # noqa
        return application_vendor

    @classmethod
    def application_title(cls) -> str:  # noqa
        return application_title

    @classmethod
    def application_description(cls) -> str:  # noqa
        return application_description

    @classmethod
    def application_tagline(cls) -> str:  # noqa
        return application_tagline

    @classmethod
    def application_licence(cls) -> str:  # noqa
        return application_licence

    @classmethod
    def application_homepage(cls) -> str:  # noqa
        return application_homepage

    @classmethod
    def application_copyright_year(cls) -> str:  # noqa
        return application_copyright_year

    @classmethod
    def application_copyright_holder(cls) -> str:  # noqa
        return application_copyright_holder

    @property
    def cache_dir(self) -> Path:
        """Gets the current instance's cache dir.

        Returns:
            A Path object to the cache directory
        """
        return self._config.cache_dir


def factory() -> Valiant:
    """Generates a valiant instance.

    Returns:
        A freshly built valiant
    """
    return Valiant(config=Config(default_config))
