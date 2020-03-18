"""Tests for the Python classifier assets."""

import pytest

from valiant.util import Classifier


@pytest.mark.parametrize(
    ("test_input,expected"),
    [
        (
            "Development Status :: 6 - Mature",
            Classifier(category="Development Status", value="6 - Mature"),
        ),
        (
            " License :: Nokia Open Source License (NOKOS) ",
            Classifier(category="License", value="Nokia Open Source License (NOKOS)"),
        ),
        (
            "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",  # noqa: B950
            Classifier(
                category="License",
                subcategory="OSI Approved",
                value="GNU Library or Lesser General Public License (LGPL)",
            ),
        ),
        (
            "Topic :: Text Editors :: Integrated Development Environments (IDE)",
            Classifier(
                category="Topic",
                subcategory="Text Editors",
                value="Integrated Development Environments (IDE)",
            ),
        ),
    ],
)
def test_parse_classifier(test_input: str, expected: Classifier) -> None:
    """Testing classifier parsing over a variety of input.

    Args:
        test_input: String version of the classifier.
        expected: The intended Classifier instance.
    """
    classifier = Classifier.parse(test_input)
    assert classifier == expected


@pytest.mark.parametrize(
    "test_input",
    [
        "BadString",
        "NoValue ::",
        "Bad ;; Delimiter",
        "Too :: Many :: Classifiers :: Nooo",
    ],
)
def test_parse_classifier_bad_input(test_input: str) -> None:
    """Test handling of bad input.

    Args:
        test_input: String version of the classifier.
    """
    with pytest.raises(ValueError):
        Classifier.parse(test_input)
