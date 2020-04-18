"""Core plugin management types.

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
from importlib.metadata import EntryPoint, entry_points
from typing import Any, Callable, Dict, Generator, List, Mapping, Optional, Set, Tuple

from valiant.log import get_logger

from .plugin import PluginWrapper

log = get_logger()


class PluginManager(object):  # pylint: disable=too-few-public-methods
    """Find and manage plugins consistently."""

    def __init__(
        self, namespace: str, local_plugins: Optional[Mapping[str, str]] = None
    ) -> None:
        """Initialize the manager.

        Args:
            namespace: Namespace of the plugins to manage, e.g., 'flake8.extension'.
            local_plugins: Plugins from config (as "X = path.to:Plugin" strings).
        """
        self.namespace = namespace
        self.plugins: Dict[str, PluginWrapper] = {}
        self.names: List[str] = []
        self._load_local_plugins(local_plugins or {})
        self._load_entrypoint_plugins()

    def _load_local_plugins(self, local_plugins: Mapping[str, str]) -> None:
        """Load local plugins from config.

        Args:
            local_plugins: x.
        """
        for name, entry_str in local_plugins.items():
            """
            I've set mypy to ignore an error on the line below:
                - Unexpected keyword argument "group" for "EntryPoint"

            As the EntryPoint definition I see is a NamedTuple with "group" being
            an attribute (Python 3.8 importlib):

                class EntryPoint(
                    collections.namedtuple('EntryPointBase', 'name value group')):
            """
            entry_point = EntryPoint(  # type: ignore
                name=name, value=entry_str, group=self.namespace
            )
            self._load_plugin_from_entrypoint(entry_point, local=True)

    def _load_entrypoint_plugins(self) -> None:
        log.info(f"Loading entry-points for '{self.namespace}'.")
        eps = entry_points().get(self.namespace, ())

        for entry_point in sorted(frozenset(eps)):
            self._load_plugin_from_entrypoint(entry_point)

    def _load_plugin_from_entrypoint(
        self, entry_point: EntryPoint, local: bool = False
    ) -> None:
        """Load a plugin from a setuptools EntryPoint.

        Args:
            entry_point: EntryPoint to load plugin from.
            local: Is this a repo-local plugin?
        """
        name = entry_point.name
        self.plugins[name] = PluginWrapper(name, entry_point, local=local)
        self.names.append(name)
        log.debug(f"Loaded {self.plugins[name]} for plugin '{name}'.")

    def map(
        self, func: Callable, *args: Any, **kwargs: Any
    ) -> Generator[Any, None, None]:
        """Call `func` with the plugin and *args and **kwargs after.

        This yields the return value from ``func`` for each plugin.

        Signature for func should at least be:

            def myfunc(plugin):
                pass

        Any extra positional or keyword arguments specified with map will
        be passed along to this function after the plugin. The plugin
        passed is a :class:`~flake8.plugins.manager.Plugin`.

        Args:
            func: Function to call with each plugin.
            *args: Positional arguments to pass to ``func`` after each plugin.
            **kwargs: Keyword arguments to pass to ``func`` after each plugin.

        Yields:
            The result of func
        """
        for name in self.names:
            yield func(self.plugins[name], *args, **kwargs)

    def versions(self) -> Generator[Tuple[str, str], None, None]:
        """Generate the versions of plugins.

        Yields:
            Tuples of the plugin_name and version
        """
        plugins_seen: Set[str] = set()
        for entry_point_name in self.names:
            plugin = self.plugins[entry_point_name]
            plugin_name = plugin.plugin_name
            plugin_version = plugin.plugin_version
            if plugin.plugin_name in plugins_seen:
                continue
            plugins_seen.add(plugin_name)
            yield (plugin_name, plugin_version)
