"""Configuration for Valiant."""
from pathlib import Path
from typing import Optional


class Config:
    """Configuration object."""

    def __init__(self, cache_dir: str = None):
        """Constructor.

        Args:
            cache_dir: Used by Valiant to cache assets
        """
        self._cache_dir: Optional[Path] = None
        if cache_dir:
            self._cache_dir = Path(cache_dir)

    @property
    def cache_dir(self) -> Optional[Path]:
        """Path to the cache."""
        return self._cache_dir  # noqa: DAR201

    @classmethod
    def load_default_config(cls) -> "Config":
        """Returns an instance with the defaults.

        Returns:
            A default Config instance.
        """
        return Config()
