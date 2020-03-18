"""Tests for the Valiant Config class."""

from pathlib import Path

from valiant.config import Config


def test_default_config() -> None:
    """Checks default config."""
    c = Config.load_default_config()
    assert c.cache_dir is None


def test_empty_config() -> None:
    """Checks config with no initial settings."""
    c = Config()
    assert c.cache_dir is None


def test_basic_config() -> None:
    """Basic config test."""
    c = Config(cache_dir="/var/cache")
    assert c.cache_dir == Path("/var/cache")
