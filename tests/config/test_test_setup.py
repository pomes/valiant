"""Tests that the test setup is working as expected.

Who tests the tester? This guy.


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

from appdirs import AppDirs


def test_override_appdirs(tmp_path: Path, appdirs: AppDirs) -> None:
    """Tests that AppDirs was patched correctly and pointing to a tmp_path."""
    assert appdirs.user_data_dir == (tmp_path / "user_data_dir")
    assert appdirs.user_config_dir == (tmp_path / "user_config_dir")
    assert appdirs.user_cache_dir == (tmp_path / "user_cache_dir")
    assert appdirs.user_log_dir == (tmp_path / "user_log_dir")

    assert appdirs.site_data_dir == (tmp_path / "site_data_dir")
    assert appdirs.site_config_dir == (tmp_path / "site_config_dir")


def test_appdirs_created(appdirs_created: AppDirs) -> None:
    """Tests that the appdirs are created for tests."""
    assert appdirs_created.user_data_dir.exists()
    assert appdirs_created.user_config_dir.exists()
    assert appdirs_created.user_cache_dir.exists()
    assert appdirs_created.user_log_dir.exists()

    assert appdirs_created.site_data_dir.exists()
    assert appdirs_created.site_config_dir.exists()
