"""The primary entrypoint into the valiant project."""
import os

from .valiant import Valiant, factory


_ROOT = os.path.dirname(os.path.realpath(__file__))
