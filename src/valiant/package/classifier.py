"""Utility resources for classifiers.

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
