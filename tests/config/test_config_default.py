"""Tests for the Valiant Config class.

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

import pytest

from valiant.config import ConfigBuilder
from valiant.repositories import RepositoryConfiguration
from valiant.repositories.pypi import PyPiRepository

from .util import get_config_instance


def test_default_config(
    tmp_path: Path,
    config_default_builder: ConfigBuilder,
    pypi_repo: PyPiRepository,
    valiant_app_name: str,
    valiant_version: str,
) -> None:
    """Basic config test making sure the defaults come through correctly."""
    from string import Template

    c = get_config_instance(config_default_builder)

    assert c.configuration_dir == tmp_path / "user_config_dir"
    assert c.cache_dir == tmp_path / "user_cache_dir"
    assert c.log_dir == tmp_path / "user_log_dir"

    # Repository config
    assert c.default_repository == "pypi"
    assert c.default_repository_name == "pypi"
    assert c.repository_configurations == {"pypi": pypi_repo}
    assert c.default_repository_configuration == pypi_repo
    assert c.repository_names == ["pypi"]
    assert c.get_repository_configuration("pypi") == pypi_repo

    # Report config
    assert c.default_reports == set(["basic", "safety", "spdx"])

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


def test_default_config_to_dict(
    tmp_path: Path,
    config_default_builder: ConfigBuilder,
    pypi_repo: RepositoryConfiguration,
    valiant_app_name: str,
    valiant_version: str,
) -> None:
    """Test the to_dict is an accurate representation."""
    d = get_config_instance(config_default_builder).to_dict()["tool"]["valiant"]
    assert d["configuration_dir"] == str(tmp_path / "user_config_dir")
    assert d["cache_dir"] == str(tmp_path / "user_cache_dir")
    assert d["log_dir"] == str(tmp_path / "user_log_dir")

    # Repos
    assert d["default_repository"] == "pypi"
    pypi_dict = pypi_repo.to_dict()
    assert d["repository_configurations"]["pypi"] == pypi_dict
    assert d["repository_configurations"]["pypi"]["base_url"] == pypi_dict["base_url"]
    assert d["repository_configurations"]["pypi"]["name"] == pypi_dict["name"]
    assert (
        d["repository_configurations"]["pypi"]["repository_type"]
        == pypi_dict["repository_type"]
    )
    assert d["repository_configurations"]["pypi"]["username"] == pypi_dict["username"]
    assert d["repository_configurations"]["pypi"]["password"] == pypi_dict["password"]
    assert d["repository_configurations"]["pypi"]["token"] == pypi_dict["token"]

    # Reports
    assert not [i for i in d["default_reports"] if i not in ["basic", "safety", "spdx"]]

    # Logging
    assert not d["logging_configuration_file"]

    # Requests Cache
    assert d["requests_cache"]["backend"] == "sqlite"
    assert d["requests_cache"]["expire_after"] == 86400
    assert (
        d["requests_cache"]["file"]
        == f"$cache_dir/{valiant_app_name}-{valiant_version}-requests-cache"
    )


def test_config_access_bad_repo_name(config_default_builder: ConfigBuilder,) -> None:
    """Attempt to get a repo not included in the default setup."""
    with pytest.raises(KeyError):
        get_config_instance(config_default_builder).get_repository_configuration(
            "DoesNotExist"
        )
