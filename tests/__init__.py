"""Valiant tests."""
from typing import Any

MonkeyPatch = Any


class MockResponse:
    """Basic mock for requests.get response."""

    def __init__(
        self, status_code: int, json_data: Any, from_cache: bool = True
    ):  # noqa: D107
        self.status_code = status_code
        self.json_data = json_data
        self._from_cache = from_cache

    def json(self) -> Any:  # noqa: D102
        return self.json_data

    @property
    def from_cache(self) -> Any:  # noqa: D102
        return self._from_cache
