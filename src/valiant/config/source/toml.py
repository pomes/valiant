"""TOML ConfigurationSource."""
from pathlib import Path
from typing import Any, Dict, cast

from valiant.config import (
    BuildResultStatus,
    ConfigurationSource,
    ConfigurationSourceBuildResult,
)


class TomlSource(ConfigurationSource):
    """Reads config from a toml file."""

    def __init__(self, path: Path, optional: bool = True) -> None:
        """Initialiser.

        Args:
            path: the path to the TOML file
            optional: False is this file must be read, True otherwise
        """
        self._path = path
        self._optional = optional

    def build(self) -> ConfigurationSourceBuildResult:  # noqa: D102
        import toml

        if not self._optional and not self._path.exists():
            raise ValueError(
                f"The required configuration file does not exist: {self._path}"
            )

        if self._path.exists():
            return ConfigurationSourceBuildResult(
                source=str(self._path),
                status=BuildResultStatus.READ.value,
                result=cast(Dict[str, Any], toml.load(self._path)),
            )
        else:
            return ConfigurationSourceBuildResult(
                source=str(self._path),
                status=BuildResultStatus.NOT_READ.value,
                result={},
            )
