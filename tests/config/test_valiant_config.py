"""Tests the Valiant configuration.

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
import os

from pathlib import Path

import py
import pytest

from valiant.repositories.pypi import PyPiRepository

from .util import FIXTURE_DIR


def test_valiant_default_config_builder(
    tmp_path: Path,
    pypi_repo: PyPiRepository,
    valiant_app_name: str,
    valiant_version: str,
) -> None:
    """Tests the config builder with no config file overlays."""
    from string import Template
    from valiant.config.util import create_valiant_builder
    from .util import get_config_instance

    vb = create_valiant_builder(
        include_pyproject=False, include_user_config=False, include_site_config=False
    )
    c = get_config_instance(vb)

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


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "site_config_dir"), keep_top_dir=True,
)
def test_valiant_site_config_builder(datafiles: py.path,) -> None:
    """Tests the config builder with a site config file overlay."""
    from valiant.config.util import create_valiant_builder
    from .util import get_config_instance

    vb = create_valiant_builder(include_pyproject=False)
    c = get_config_instance(vb)
    datafiles.listdir()
    assert c.configuration_dir == Path("/tmp/valiant_test/opt/etc")  # noqa: S108
    assert c.cache_dir == Path("/tmp/valiant_test/opt/var/cache")  # noqa: S108
    assert c.log_dir == Path("/tmp/valiant_test/opt/var/log")  # noqa: S108
    assert c.default_reports == set(["basic"])
    assert c.local_plugin_paths == []
    assert c.local_report_plugins == {}


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "user_config_dir"), keep_top_dir=True,
)
def test_valiant_user_config_builder(datafiles: py.path,) -> None:
    """Tests the config builder with a user config file overlay."""
    from valiant.config.util import create_valiant_builder
    from .util import get_config_instance

    vb = create_valiant_builder(include_pyproject=False)
    c = get_config_instance(vb)

    assert c.configuration_dir == Path("/tmp/valiant_test/usr/local/etc")  # noqa: S108
    assert c.cache_dir == Path("/tmp/valiant_test/usr/local/var/cache")  # noqa: S108
    assert c.log_dir == Path("/tmp/valiant_test/usr/local/var/log")  # noqa: S108
    assert c.default_reports == set(["safety", "spdx"])
    assert c.local_plugin_paths == ["/usr/local/lib"]
    assert c.local_report_plugins == {"report1": "mypkg.Reporter:Report1"}


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "user_config_dir"),
    os.path.join(FIXTURE_DIR, "site_config_dir"),
    keep_top_dir=True,
)
def test_valiant_user_and_site_config_builder(datafiles: py.path,) -> None:
    """Tests the config builder with site and user config file overlays."""
    from valiant.config.util import create_valiant_builder
    from .util import get_config_instance

    vb = create_valiant_builder(include_pyproject=False)
    c = get_config_instance(vb)

    assert c.configuration_dir == Path("/tmp/valiant_test/usr/local/etc")  # noqa: S108
    assert c.cache_dir == Path("/tmp/valiant_test/usr/local/var/cache")  # noqa: S108
    assert c.log_dir == Path("/tmp/valiant_test/usr/local/var/log")  # noqa: S108
    assert c.default_reports == set(["safety", "spdx"])
    assert c.local_plugin_paths == ["/usr/local/lib"]
    assert c.local_report_plugins == {"report1": "mypkg.Reporter:Report1"}


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "pyproject.toml"), keep_top_dir=True,
)
@pytest.mark.usefixtures("create_and_cwd_test_directory")
def test_valiant_pyproject_config_builder(
    pypi_repo: PyPiRepository,
    valiant_app_name: str,
    valiant_version: str,
    datafiles: py.path,
) -> None:
    """Tests the config builder with a pyproject file overlay."""
    import shutil
    from valiant.config.util import create_valiant_builder
    from .util import get_config_instance

    # Copy over pyproject.toml
    cwd = Path.cwd()
    assert os.listdir(cwd) == []
    shutil.copy(src=Path(datafiles, "pyproject.toml"), dst=cwd)
    assert os.listdir(cwd) == ["pyproject.toml"]

    vb = create_valiant_builder()
    c = get_config_instance(vb)

    assert c.configuration_dir == Path("/tmp/valiant_test/project/etc")  # noqa: S108
    assert c.cache_dir == Path("/tmp/valiant_test/project/var/cache")  # noqa: S108
    assert c.log_dir == Path("/tmp/valiant_test/project/var/log")  # noqa: S108
    assert c.default_reports == set(["safety"])
    assert c.local_plugin_paths == ["/usr/local/lib", "./project_lib"]
    assert c.local_report_plugins == {"project_report": "myprojectpkg.Reporter:Report1"}


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "pyproject.toml"),
    os.path.join(FIXTURE_DIR, "user_config_dir"),
    os.path.join(FIXTURE_DIR, "site_config_dir"),
    keep_top_dir=True,
)
@pytest.mark.usefixtures("create_and_cwd_test_directory")
def test_valiant_all_config_builder(
    pypi_repo: PyPiRepository,
    valiant_app_name: str,
    valiant_version: str,
    datafiles: py.path,
) -> None:
    """Tests the config builder with the pyproject, user and site file overlays."""
    import shutil
    from valiant.config.util import create_valiant_builder
    from .util import get_config_instance

    # Copy over pyproject.toml
    assert os.listdir(os.getcwd()) == []
    shutil.copy(os.path.join(datafiles, "pyproject.toml"), os.getcwd())
    assert os.listdir(os.getcwd()) == ["pyproject.toml"]

    vb = create_valiant_builder()
    c = get_config_instance(vb)

    assert c.configuration_dir == Path("/tmp/valiant_test/project/etc")  # noqa: S108
    assert c.cache_dir == Path("/tmp/valiant_test/project/var/cache")  # noqa: S108
    assert c.log_dir == Path("/tmp/valiant_test/project/var/log")  # noqa: S108
    assert c.default_reports == set(["safety"])
    assert c.local_plugin_paths == ["/usr/local/lib", "./project_lib"]
    assert c.local_report_plugins == {"project_report": "myprojectpkg.Reporter:Report1"}
