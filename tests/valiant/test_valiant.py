"""Basic test suite."""
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


def test_config_empty() -> None:
    """Testing valiant configuration."""
    conf = Config()
    v = factory(conf)
    assert v.cache_dir is None
