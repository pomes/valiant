"""Test the Dictionizer!"""
from typing import Dict
from valiant.util import Dictionizer


class TestClass(Dictionizer):  # noqa:DAR101
    def to_dict(self) -> Dict:  # noqa:DAR101
        return {
            "name": "fred",
            "pets": ["matlida", "riff"],
            "favourites": {"colour": "blue", "fruit": "banana"},
        }


def test_dictionizer_dict() -> None:
    """Check the base dict values."""
    d = TestClass().to_dict()
    assert d["name"] == "fred"
    assert d["pets"] == ["matlida", "riff"]
    assert d["favourites"]["colour"] == "blue"
    assert d["favourites"]["fruit"] == "banana"


def test_dictionizer_json() -> None:
    """Check the base json values."""
    import json

    j = json.loads(TestClass().to_json())
    assert j
    assert j["name"] == "fred"
    assert j["pets"] == ["matlida", "riff"]
    assert j["favourites"]["colour"] == "blue"
    assert j["favourites"]["fruit"] == "banana"
