"""Basic test suite."""
from pathlib import Path

import pytest

from valiant import Valiant
from valiant.config import ConfigBuilder
from valiant.config.source import MappingSource


@pytest.fixture(scope="function")
def config_builder(tmp_path: Path) -> ConfigBuilder:
    """Create a builder ready for test runs.

    Returns:
        ConfigBuilder instance.
    """
    import os
    from valiant.config.util import create_valiant_builder

    builder = create_valiant_builder(
        include_pyproject=False, include_user_config=False, include_site_config=False
    )
    builder.add_source(
        MappingSource(
            {
                "tool": {
                    "valiant": {
                        "configuration_dir": os.path.join(tmp_path, "etc"),
                        "cache_dir": os.path.join(tmp_path, "var"),
                        "log_dir": os.path.join(tmp_path, "log"),
                    }
                }
            }
        )
    )
    return builder


@pytest.fixture(scope="function")
def configured_valiant(config_builder: ConfigBuilder) -> Valiant:
    """Returns a Valiant instance with testing config ready.

    # noqa:DAR201
    # noqa:DAR401
    """
    from valiant.config.util import ConfigMapBuilder

    conf_map = config_builder.build()
    if conf_map:
        conf = ConfigMapBuilder.generate_valiant_config_from_map(conf_map)
        return Valiant(conf)
    else:
        raise ValueError("Could not build you a Valiant")


def test_application_details(configured_valiant: Valiant) -> None:
    """Validate the general app info."""
    v = configured_valiant
    assert v.application_version == "0.2.0"
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
    with pytest.raises(TypeError):
        Valiant()  # type: ignore


def test_config_default(configured_valiant: Valiant) -> None:
    """Tests the factory defaults."""
    v = configured_valiant
    assert v.cache_dir is not None
    assert v.configuration_dir is not None
