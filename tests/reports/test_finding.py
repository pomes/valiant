"""Basic tests for the Finding class.

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
from dataclasses import dataclass
from typing import Dict, List

import pytest

from valiant.package import PackageCoordinates
from valiant.reports import Finding, FindingCategory, FindingLevel
from valiant.util import Dictionizer


@dataclass
class BasicTestData(Dictionizer):  # noqa:D101
    name: str
    age: int
    hobbies: List[str]
    journal: Dict[str, str]

    def to_dict(self) -> Dict:  # noqa:D102
        import dataclasses

        return dataclasses.asdict(self)


@pytest.fixture
def finding() -> Finding:
    """Just a sample finding."""
    return Finding(  # noqa:DAR201
        coordinates=PackageCoordinates(
            name="test", version="1.0.0", repository_url="http://www.example.com"
        ),
        id="001",
        level=FindingLevel.INFO,
        category=FindingCategory.PROJECT.value,
        title="A test finding",
        message="This is a test",
        data=BasicTestData(
            name="Bill",
            age=32,
            hobbies=["sailing", "sleeping", "sewing"],
            journal={"Day 1": "I am sailing", "Day 2": "I am sleeping"},
        ),
        url="http://www.example.com",
    )


def test_to_dict(finding: Finding) -> None:
    """Basic test of the Dictionizer trait."""
    d = finding.to_dict()
    assert d["id"] == "001"
    assert d["level"] == FindingLevel.INFO.value
    assert d["category"] == "project"
    assert d["title"] == "A test finding"
    assert d["message"] == "This is a test"
    assert d["url"] == "http://www.example.com"
    data = d["data"]
    assert data["name"] == "Bill"
    assert data["age"] == 32
    assert data["hobbies"] == ["sailing", "sleeping", "sewing"]
    assert data["journal"]["Day 1"] == "I am sailing"


def test_to_json(finding: Finding) -> None:
    """Basic test of the Dictionizer trait."""
    import json

    j = finding.to_json()

    d = json.loads(j)
    assert d["id"] == "001"
    assert d["level"] == FindingLevel.INFO.value
    assert d["category"] == "project"
    assert d["title"] == "A test finding"
    assert d["message"] == "This is a test"
    assert d["url"] == "http://www.example.com"
    data = d["data"]
    assert data["name"] == "Bill"
    assert data["age"] == 32
    assert data["hobbies"] == ["sailing", "sleeping", "sewing"]
    assert data["journal"]["Day 1"] == "I am sailing"
