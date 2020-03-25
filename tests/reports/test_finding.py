"""Basic tests for the Finding class."""
from dataclasses import dataclass
from typing import Dict, List

import pytest

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
