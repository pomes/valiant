"""Test the Dictionizer!

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
"""
from typing import Dict

from valiant.util import Dictionizer


class TestClass(Dictionizer):  # noqa:D101
    def to_dict(self) -> Dict:  # noqa:D102
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
