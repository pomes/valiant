"""Utility resources for classifiers."""
from dataclasses import dataclass
from typing import List, Optional


SEPARATOR = " :: "


@dataclass
class Classifier:
    """An individual python classifier.

    See: https://www.python.org/dev/peps/pep-0301/#distutils-trove-classification
    See: https://pypi.org/classifiers/
    """

    category: str
    value: str
    subcategory: Optional[str] = None

    @staticmethod
    def parse(value: str) -> "Classifier":
        """Parses a classifier string.

        Args:
            value: The classifier string.

        Returns:
            A new Classifier instance based on value.

        Raises:
            ValueError: If value doesn't parse to 2 or 3 segments.
        """
        components: List[str] = value.split(SEPARATOR)

        ln = len(components)

        if ln not in [2, 3]:
            raise ValueError(f"Expected 2 or 3 segments, got {ln}")

        subcategory = None

        if ln == 3:
            subcategory = components[1].strip()

        return Classifier(
            category=components[0].strip(),
            value=components[-1].strip(),
            subcategory=subcategory,
        )
