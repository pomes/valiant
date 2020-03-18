"""Make sure abstract classes don't do anything."""

import pytest

from valiant.repositories import BaseRepository


def test_base_repository() -> None:
    """Ensure that instantiating the class raises TypeError."""
    with pytest.raises(TypeError):
        BaseRepository()
