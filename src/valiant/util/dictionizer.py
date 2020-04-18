"""Trait for dictionary and json translation.

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
