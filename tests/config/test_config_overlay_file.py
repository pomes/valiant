"""Tests config with non-default config sources.

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
from pathlib import Path
import os
from typing import Any

import py
import pytest

from valiant.config import ConfigBuilder
from valiant.repositories.pypi import PyPiRepository

from .util import FIXTURE_DIR, get_config_instance


def test_missing_required_overlay_file(config_default_builder: ConfigBuilder) -> None:
    """Provides an explicit TOML source that doesn't exists - should raise an exception."""
    from valiant.config.source import TomlSource

    # The exception should only occur when build() is called
    config_default_builder.add_source(
        TomlSource(Path("/i/do/not/exist.toml"), optional=False)
    )
    with pytest.raises(ValueError):
        config_default_builder.build()


@pytest.mark.usefixtures("clean_up_tmp_folder")
@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "basic.toml"))
def test_explicit_file_overlay(
    config_default_builder: ConfigBuilder, datafiles: py.path,
) -> None:
    """Provides an explicit TOML source to overlay the default config."""
    from valiant.config.source import TomlSource

    config_default_builder.add_source(
        TomlSource(Path(os.path.join(FIXTURE_DIR, "basic.toml")), optional=False)
    )

    c = get_config_instance(config_default_builder)

    assert c.configuration_dir == Path("/tmp/valiant_test/etc")
    assert c.cache_dir == Path("/tmp/valiant_test/var/cache")
    assert c.log_dir == Path("/tmp/valiant_test/var/log")
    assert c.default_reports == set(["basic", "spdx"])


@pytest.mark.usefixtures("clean_up_tmp_folder")
@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "config_output.toml"))
def test_explicit_file_overlay_from_valiant_config(
    config_default_builder: ConfigBuilder,
    pypi_repo: PyPiRepository,
    valiant_app_name: str,
    valiant_version: str,
    datafiles: py.path,
) -> None:
    """Provides an explicit TOML source to overlay the default config."""
    from string import Template
    from valiant.config.source import TomlSource

    config_default_builder.add_source(
        TomlSource(
            Path(os.path.join(FIXTURE_DIR, "config_output.toml")), optional=False
        )
    )

    c = get_config_instance(config_default_builder)

    assert c.configuration_dir == Path("/tmp/valiant_test/etc")
    assert c.cache_dir == Path("/tmp/valiant_test/var/cache")
    assert c.log_dir == Path("/tmp/valiant_test/var/log")
    assert c.default_reports == set(["basic", "spdx", "safety"])

    # Repository config
    assert c.default_repository == "pypi"
    assert c.default_repository_name == "pypi"
    assert c.repository_configurations == {"pypi": pypi_repo}
    assert c.default_repository_configuration == pypi_repo
    assert c.repository_names == ["pypi"]
    assert c.get_repository_configuration("pypi") == pypi_repo

    # Local plugins should be empty
    assert c.local_plugin_paths == []
    assert c.local_report_plugins == {}

    # Logging
    assert not c.logging_configuration_file

    # Requests cache
    assert c.requests_cache["backend"] == "sqlite"
    assert c.requests_cache["expire_after"] == 86400
    assert (
        Template(str(c.requests_cache["file"])).substitute(
            log_dir=c.log_dir,
            cache_dir=c.cache_dir,
            configuration_dir=c.configuration_dir,
        )
        == f"{c.cache_dir}/{valiant_app_name}-{valiant_version}-requests-cache"
    )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "logging.conf"))
def test_basic_overlay_mapping(
    config_default_builder: ConfigBuilder, datafiles: py.path
) -> None:
    """Manually adds a config dict with a logging_configuration_file."""
    from valiant.config.source import MappingSource

    config_default_builder.add_source(
        MappingSource(
            {
                "tool": {
                    "valiant": {
                        "logging_configuration_file": Path(FIXTURE_DIR, "logging.conf")
                    }
                }
            }
        )
    )
    c = get_config_instance(config_default_builder)
    assert c.logging_configuration_file == Path(FIXTURE_DIR, "logging.conf")


@pytest.mark.usefixtures("clean_up_tmp_folder")
@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "basic_logfile.toml"),)
def test_basic_overlay_file(
    config_default_builder: ConfigBuilder, datafiles: py.path, copy_test_files: Any,
) -> None:
    """Manually adds a config dict with a logging_configuration_file."""
    from valiant.config.source import TomlSource

    config_default_builder.add_source(
        TomlSource(
            Path(os.path.join(FIXTURE_DIR, "basic_logfile.toml")), optional=False
        )
    )
    c = get_config_instance(config_default_builder)
    assert c.logging_configuration_file == Path("/tmp/valiant_test_data/logging.conf")
