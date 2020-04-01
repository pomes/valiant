"""Trait for dictionary and json translation."""
from abc import ABC, abstractmethod
from typing import Dict


class Dictionizer(ABC):
    """Implementers provide a dict and json rendition."""

    @abstractmethod
    def to_dict(self) -> Dict:
        """Convert the instance to a dictionary format."""
        raise NotImplementedError()  # noqa:DAR401

    def to_json(self) -> str:
        """Convert the instance to JSON format."""  # noqa:DAR201
        import json

        return json.dumps(self.to_dict())

    def to_toml(self) -> str:
        """Convert the instance to TOML format."""  # noqa:DAR201
        import toml

        return toml.dumps(self.to_dict())
