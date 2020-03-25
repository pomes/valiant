"""Utility resources for classifiers."""
from dataclasses import asdict, dataclass
from typing import Dict, List

from valiant.util import Dictionizer

SEPARATOR = " :: "

CLASSIFIER_CATEGORY_LICENSE = "License"
CLASSIFIER_CATEGORY_DEVELOPMENT_STATUS = "Development Status"
CLASSIFIER_CATEGORY_ENVIRONMENT = "Environment"
CLASSIFIER_CATEGORY_FRAMEWORK = "Framework"
CLASSIFIER_CATEGORY_INTENDED_AUDIENCE = "Intended Audience"
CLASSIFIER_CATEGORY_NATURAL_LANGUAGE = "Natural Language"
CLASSIFIER_CATEGORY_OPERATING_SYSTEM = "Operating System"
CLASSIFIER_CATEGORY_PROGRAMMING_LANGUAGE = "Programming Language"
CLASSIFIER_CATEGORY_TOPIC = "Topic"
CLASSIFIER_CATEGORY_TYPING = "Typing"


@dataclass
class Classifier(Dictionizer):
    """An individual python classifier.

    See: https://www.python.org/dev/peps/pep-0301/#distutils-trove-classification
    See: https://pypi.org/classifiers/
    """

    original: str
    category: str
    value: str
    subcategories: List[str]

    def to_dict(self) -> Dict:  # noqa:D102
        return asdict(self)

    @staticmethod
    def parse(value: str) -> "Classifier":
        """Parses a classifier string.

        Args:
            value: The classifier string.

        Returns:
            A new Classifier instance based on value.

        Raises:
            ValueError: If value doesn't parse to at least 2 segments.
        """
        components: List[str] = value.split(SEPARATOR)

        subcategories = []

        if len(components) < 2:
            raise ValueError(f"Could not parse classifier: {value}")
        elif len(components) >= 3:
            for sc in components[1:-1]:
                subcategories.append(sc.strip())

        return Classifier(
            original=value,
            category=components[0].strip(),
            value=components[-1].strip(),
            subcategories=subcategories,
        )
