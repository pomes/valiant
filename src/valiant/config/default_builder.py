"""An easy win for starting a config."""
from typing import Callable, Optional
from valiant.config.builder import ConfigBuilder, ConfigMap


class DefaultConfigBuilder(ConfigBuilder):
    """A builder that is based on sensible config sources.

    The following sources are used (each overlaying the previous):

        1. An initial dictionary can be provided to form a baseline
        2. A `config.toml` file from the site config dir is used (if it exists)
        3. A `config.toml` file from the user's config dir is used (if it exists)
        4. A `pyproject.toml` file is used if it exists in the current directory

    See: https://pypi.org/project/appdirs/
    """

    def __init__(
        self,
        initial_data: Optional[ConfigMap] = None,
        vendor: str = "unknown",
        app: str = "unknown",
        version: str = "0",
        include_pyproject: bool = True,
        include_user_config: bool = True,
        include_site_config: bool = True,
        filter: Callable[[ConfigMap], ConfigMap] = lambda d: d,
    ) -> None:
        """Initialiser.

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
        """
        import os
        import sys
        from pathlib import Path
        from appdirs import AppDirs
        from valiant.config.source import TomlSource, MappingSource

        super().__init__(filter)
        if initial_data:
            self.add_source(MappingSource(initial_data))

        dirs = AppDirs(appname=app, appauthor=vendor, version=version)
        if include_site_config:
            self.add_source(TomlSource(Path(dirs.site_config_dir, "config.toml")))

        if include_user_config:
            self.add_source(TomlSource(Path(dirs.user_config_dir, "config.toml")))

        if include_pyproject:
            cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
            self.add_source(TomlSource(Path(cwd, "pyproject.toml")))
