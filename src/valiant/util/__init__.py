"""Utility oddjobs."""
from .dictionizer import Dictionizer

from enum import Enum


class NoValue(Enum):
    """As per https://docs.python.org/3/library/enum.html#omitting-values."""

    def __repr__(self):  # noqa:D105
        return "<%s.%s>" % (self.__class__.__name__, self.name)
