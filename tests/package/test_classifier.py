"""Tests for the Python classifier assets."""

import pytest

from valiant.package import Classifier


@pytest.mark.parametrize(
    ("test_input,expected"),
    [
        (
            "Development Status :: 6 - Mature",
            Classifier(
                original="Development Status :: 6 - Mature",
                category="Development Status",
                subcategories=[],
                value="6 - Mature",
            ),
        ),
        (
            " License :: Nokia Open Source License (NOKOS) ",
            Classifier(
                original=" License :: Nokia Open Source License (NOKOS) ",
                category="License",
                subcategories=[],
                value="Nokia Open Source License (NOKOS)",
            ),
        ),
        (
            "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",  # noqa: B950
            Classifier(
                original="License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",  # noqa: B950
                category="License",
                subcategories=["OSI Approved"],
                value="GNU Library or Lesser General Public License (LGPL)",
            ),
        ),
        (
            "Topic :: Text Editors :: Integrated Development Environments (IDE)",
            Classifier(
                original="Topic :: Text Editors :: Integrated Development Environments (IDE)",
                category="Topic",
                subcategories=["Text Editors"],
                value="Integrated Development Environments (IDE)",
            ),
        ),
        (
            "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
            Classifier(
                original="Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
                category="Topic",
                subcategories=["Internet", "WWW/HTTP", "Site Management"],
                value="Link Checking",
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


def test_classifier_to_dict() -> None:
    """Test the conversion to a dictionary."""
    d = Classifier(
        original="Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
        category="Topic",
        subcategories=["Internet", "WWW/HTTP", "Site Management"],
        value="Link Checking",
    ).to_dict()

    assert d["category"] == "Topic"
    assert d["value"] == "Link Checking"
    assert d["subcategories"] == ["Internet", "WWW/HTTP", "Site Management"]
    assert (
        d["original"]
        == "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking"
    )


@pytest.mark.parametrize(
    "test_input", ["BadString", "NoValue ::", "Bad ;; Delimiter"],
)
def test_parse_classifier_bad_input(test_input: str) -> None:
    """Test handling of bad input.

    Args:
        test_input: String version of the classifier.
    """
    with pytest.raises(ValueError):
        Classifier.parse(test_input)
