"""Builds out the config using various sources.

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
from abc import ABC, abstractmethod
from collections import ChainMap, deque
from typing import Any, Callable
from typing import ChainMap as ChainMapType
from typing import Deque, Dict, Mapping, NamedTuple, Optional

from valiant.util import NoValue


"""Represents a set of configuration in a mapping (e.g. Dict) type."""
ConfigMap = Mapping[str, Any]


class BuildResultStatus(NoValue):
    """Enum for the ConfigurationSourceBuildResult status field."""

    """The resource was read."""
    READ = "Read"

    """The resource was not read."""
    NOT_READ = "Not_Read"


class ConfigurationSourceBuildResult(NamedTuple):
    """A tuple for build return values."""

    result: ConfigMap
    source: str
    status: str


class ConfigurationSource(ABC):
    """The configuration source handler base class."""

    @abstractmethod
    def build(self) -> ConfigurationSourceBuildResult:
        """Loads up a configuration."""
        raise NotImplementedError()  # noqa: DAR401


class ConfigBuilder:
    """The builder class.

    Most use-cases will kick of with `ConfigBuilder.create_default_builder()`
    and go from there. If further config sources are required, call `add_source`
    and, at the end, call `build()`.
    """

    def __init__(self, filter: Callable[[ConfigMap], ConfigMap] = lambda d: d):
        """Initializer.

        Args:
            filter: A callable (e.g. function) that accepts a dictionary as input
                and returns the filtered dictionary as output. Default is just a
                pass-through function
        """
        self._config_sources: Deque[ConfigurationSource] = deque()
        self._filter = filter

    @staticmethod
    def create_default_builder(
        initial_data: Optional[ConfigMap] = None,
        vendor: str = "unknown",
        app: str = "unknown",
        version: str = "0",
        include_pyproject: bool = True,
        include_user_config: bool = True,
        include_site_config: bool = True,
        filter: Callable[[ConfigMap], ConfigMap] = lambda d: d,
    ) -> "ConfigBuilder":
        """Sets up a builder that uses default configuration.

        Args:
            initial_data: A map of config settings that forms a baseline.
            vendor: The application vendor.
                This is generally used by filesystem-based config for directory layout
            app: The application name.
                This is generally used by filesystem-based config for directory layout
            version: The application version.
                This is generally used by filesystem-based config for directory layout
            include_pyproject: True if the local pyproject.toml file is to be read
            include_user_config: True if the user's config directory is to be used
            include_site_config: True if the system's config directory is to be used
            filter: A callable (e.g. function) that accepts a dictionary as input
                and returns the filtered dictionary as output

        Returns:
            ConfigBuilder: the default builder.
                        This is prepped with standard default sources.
        """
        from .default_builder import DefaultConfigBuilder

        return DefaultConfigBuilder(
            initial_data=initial_data,
            vendor=vendor,
            app=app,
            version=version,
            include_pyproject=include_pyproject,
            include_user_config=include_user_config,
            include_site_config=include_site_config,
            filter=filter,
        )

    def add_source(self, source: ConfigurationSource) -> "ConfigBuilder":
        """Add a configuration source.

        Each source's config will overlay the previous source when you run `build`.
        For example, say you call this in the following order:

            - add_source(A)
            - add_source(B)
            - add_source(C)

        A will be the baseline config. B will overwrite some/all of A and, in turn,
        C will overwrite the output of B's merge over A.

        Args:
            source: An instance of a ConfigurationSource

        Returns:
            The current builder instance
        """
        self._config_sources.append(source)
        return self

    def build(self) -> Optional[ChainMapType]:
        """Builds out a Config instance based on the sources.

        Returns:
            A fully-formed Config instance.
        """
        config_map: Optional[ChainMapType] = None
        build_results: Dict[str, str] = {}

        for item in self._config_sources:
            b = item.build()
            build_results[b.source] = b.status

            filtered = self._filter(b.result)

            if filtered:
                if not config_map:
                    config_map = ChainMap(filtered)
                else:
                    config_map.maps.append(filtered)

        if build_results:
            metadata = {"_builder_metadata": {"build_results": build_results}}
            if not config_map:
                config_map = ChainMap(metadata)
            else:
                config_map.maps.append(metadata)

        if config_map:
            config_map.maps.reverse()

        return config_map
