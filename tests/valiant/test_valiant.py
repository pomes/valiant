"""Basic test suite."""
from pathlib import Path
from typing import Dict, Optional

import pytest

from valiant import factory
from valiant.config import Config


def test_application_details() -> None:
    """Validate the general app info."""
    v = factory()
    assert v.application_version == "0.1.0"
    assert v.application_name == "valiant"
    assert v.application_title == "Valiant"
    assert v.application_vendor == "Pomes"
    assert v.application_tagline == "Dependency Investigations Unit"
    assert v.application_description == "Valiant helps you investigate dependencies"
    assert v.application_licence == "MIT"
    assert v.application_homepage == "https://github.com/pomes/valiant"
    assert v.application_copyright_year == 2020
    assert v.application_copyright_holder == "Duncan Dickinson"


@pytest.mark.parametrize(("test_input,expected"), [({}, None)])
def test_config_dir(test_input: Dict, expected: Optional[Path]) -> None:
    """Testing valiant configuration."""
    conf = Config(test_input)
    v = factory(conf)
    assert v.cache_dir is None
