"""Base manager for plugin types.

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

from abc import ABC, abstractmethod
from typing import Dict, List, Mapping, Optional

from valiant.log import get_logger

from .manager import PluginManager
from .plugin import PluginWrapper

log = get_logger()


class PluginTypeManager(ABC):
    """Parent class for most of the specific plugin types."""

    @property
    @abstractmethod
    def namespace(self) -> str:
        """Returns the namespace used in the entrypoint for this type of plugin."""
        raise NotImplementedError()
        # noqa:DAR401

    def __init__(self, local_plugins: Optional[Mapping[str, str]] = None) -> None:
        """Initialize the plugin type's manager.

        Args:
            local_plugins: Plugins from config file instead of entry-points

        Raises:
            ValueError: When the implementing class doesn't provide a namespace
        """
        if not self.namespace:
            raise ValueError(
                f"The PluginTypeManager subclass ({type(self)}) does not provide a namespace"
            )
        self.manager = PluginManager(self.namespace, local_plugins=local_plugins)
        self.plugins_loaded = False

    def __contains__(self, entry_point_name: str) -> bool:
        """Check if the entry-point name is in this plugin type manager."""  # noqa DAR101
        log.debug(f"Checking for '{entry_point_name} in plugin type manager.")
        return entry_point_name in self.plugins

    def __getitem__(self, name: str):
        """Retrieve a plugin by its name."""  # noqa DAR101
        log.debug(f"Retrieving plugin for '{name}.")
        return self.plugins[name]

    def get(
        self, name: str, default: Optional[PluginWrapper] = None
    ) -> Optional[PluginWrapper]:
        """Retrieve the plugin referred to by ``name`` or return the default.

        Args:
            name: Name of the plugin to retrieve.
            default: Default value to return.

        Returns:
            Plugin object referred to by name, if it exists.
        """
        if name in self:
            return self[name]
        return default

    @property
    def names(self) -> List[str]:
        """Proxy attribute to underlying manager."""
        return self.manager.names  # noqa:DAR201

    @property
    def plugins(self) -> Dict[str, PluginWrapper]:
        """Proxy attribute to underlying manager."""
        return self.manager.plugins  # noqa:DAR201

    def load_plugins(self) -> None:
        """Load all plugins of this type that are managed by this manager."""
        if self.plugins_loaded:
            return

        list(self.manager.map(lambda plugin: plugin.load_plugin()))
        # Do not set plugins_loaded if we run into an exception
        self.plugins_loaded = True
