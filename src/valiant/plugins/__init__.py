"""Valiant plugin management.

Please note that I based much of this work on the approach taken by
[Flake8](https://gitlab.com/pycqa/flake8/-/blob/master/src/flake8/plugins/manager.py).
"""
from .plugin import BasePlugin, PluginWrapper
from .type_manager import PluginTypeManager
