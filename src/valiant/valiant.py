"""Handles the valiant context."""
from pathlib import Path
from typing import Optional

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


class Valiant:
    """Provides general applications details and instance configuration."""

    def __init__(self, config: Config):
        """Fire up a new valiant.

        Args:
            config: The application configuration
        """
        self._config: Config = config

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


def factory(config: Config = None) -> Valiant:
    """Generates a valiant instance.

    TBD - this factory is rather underdone atm.

    Args:
        config: A Valiant configuration instance.

    Returns:
        A freshly built valiant
    """
    if not config:
        conf = Config()
    else:
        conf = config

    return Valiant(config=conf)
