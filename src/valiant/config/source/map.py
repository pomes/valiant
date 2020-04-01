"""Mapping configuration source."""
from valiant.config import (
    BuildResultStatus,
    ConfigurationSource,
    ConfigurationSourceBuildResult,
)
from valiant.config.builder import ConfigMap


class MappingSource(ConfigurationSource):
    """Provides a very basic dictionary source."""

    def __init__(self, map: ConfigMap) -> None:
        """Initialiser.

        Args:
            map: An overlay config dictionary
        """
        self._map = map

    def build(self) -> ConfigurationSourceBuildResult:  # noqa: D102
        return ConfigurationSourceBuildResult(
            source="dictionary", status=BuildResultStatus.READ.value, result=self._map,
        )
