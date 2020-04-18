"""Wrapper for plugins.

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


NOTICE

Parts of the code here are based on code from the Flake8 project
(https://gitlab.com/pycqa/flake8). Please review the FLAKE8_LICENCE file
(in this directory) for the original copyright and MIT licence statement.
"""

from importlib.metadata import EntryPoint
from typing import Any, Optional

from valiant.log import get_logger

from .exceptions import FailedToLoadPlugin


log = get_logger()


class BasePlugin:
    """The base for any plugin subclass."""

    name = ""
    vendor = ""
    version = ""
    display_name = ""
    url = ""

    @classmethod
    def run(cls, **kwargs: Any) -> Any:
        """This method is what Valiant will call when it gets to you."""
        raise NotImplementedError()  # noqa: DAR101, DAR401


class PluginWrapper:
    """Wrap an EntryPoint from setuptools and other logic."""

    def __init__(
        self, name: str, entry_point: EntryPoint, local: bool = False,
    ) -> None:
        """Initializer.

        Args:
            name: Name of the entry-point as it was registered with setuptools.
            entry_point: EntryPoint returned by setuptools.
            local: Is this a repo-local plugin?
        """
        self.entry_point_name = name
        self.entry_point = entry_point
        self.local = local
        self._plugin: Optional[BasePlugin] = None

    @property
    def plugin(self) -> Optional[BasePlugin]:
        """Load and return the plugin associated with the entry-point.

        This property implicitly loads the plugin and then caches it.

        Returns:
            The loaded plugin
        """
        self.load_plugin()
        return self._plugin

    @property
    def plugin_version(self) -> str:
        """Return the version of the plugin.

        Returns:
            The version of the plugin

        Raises:
            ValueError: if the underlying plugin hasn't been loaded.
        """
        if not self._plugin:
            raise ValueError(
                f"The requested plugin has not been loaded: {self.entry_point}."
            )
        return self._plugin.version

    @property
    def plugin_name(self) -> str:
        """Return the name of the plugin.

        Returns:
            The name of the plugin

        Raises:
            ValueError: if the underlying plugin hasn't been loaded.
        """
        if not self._plugin:
            raise ValueError(
                f"The requested plugin has not been loaded: {self.entry_point}."
            )
        return self._plugin.name

    @property
    def plugin_vendor(self) -> str:
        """Return the vendor of the plugin.

        Returns:
            The vendor of the plugin

        Raises:
            ValueError: if the underlying plugin hasn't been loaded.
        """
        if not self._plugin:
            raise ValueError(
                f"The requested plugin has not been loaded: {self.entry_point}."
            )

        return self._plugin.vendor

    def _load(self) -> None:
        try:
            self._plugin = self.entry_point.load()
        except ModuleNotFoundError as e:
            raise FailedToLoadPlugin(
                plugin_name=self.entry_point_name,
                entry_point=self.entry_point,
                exception=e,
            )

        if not callable(self._plugin):
            msg = f"Plugin {self._plugin} is not callable."
            log.critical(msg)
            raise TypeError(msg)

    def load_plugin(self) -> None:
        """Retrieve the plugin for this entry-point.

        This loads the plugin, stores it on the instance and then returns it.
        It does not reload it after the first time, it merely returns the
        cached plugin.

        # noqa: DAR402
        # noqa: DAR401

        Raises:
            FailedToLoadPlugin: When the plugin just can't be sorted out
        """
        if self._plugin is None:
            log.info(f"Loading plugin '{self.entry_point_name}' from entry-point.")
            try:
                self._load()
            except FailedToLoadPlugin as ftl:
                log.critical(str(ftl), entry_point=str(self.entry_point))
                raise ftl
            except Exception as load_exception:
                e = FailedToLoadPlugin(
                    plugin_name=self.entry_point_name,
                    entry_point=self.entry_point,
                    exception=load_exception,
                )
                log.critical(
                    str(e), entry_point=str(self.entry_point), exception=load_exception
                )
                raise e from load_exception

            log.info(
                f"Loaded plugin '{self.entry_point_name}' from entry-point.",
                plugin_name=self.plugin_name,
                plugin_version=self.plugin_version,
            )

    def run(self, **kwargs: Any) -> Any:
        """Call the plugin's run method with kwargs."""  # noqa:DAR101,DAR201
        if self._plugin:
            return self._plugin.run(**kwargs)
