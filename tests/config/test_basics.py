"""Test the data model basics.

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
import pytest

from valiant.config import ConfigBuilder

from .util import get_config_instance


def test_empty_config() -> None:
    """Checks config with no initial settings."""
    from valiant.config import Config

    with pytest.raises(TypeError):
        Config()  # type: ignore


def test_no_repo_config(config_default_builder: ConfigBuilder) -> None:
    """Expect failure when there are no repository_configurations."""
    from valiant.config.source import MappingSource

    config_default_builder.add_source(
        MappingSource({"tool": {"valiant": {"repository_configurations": {}}}})
    )
    with pytest.raises(ValueError):
        get_config_instance(config_default_builder)


def test_no_default_repo(config_default_builder: ConfigBuilder) -> None:  # noqa:ANN001
    """Expect failure when the default_repo isn't listed in repository_configurations."""
    from valiant.config.source import MappingSource

    config_default_builder.add_source(
        MappingSource({"tool": {"valiant": {"default_repository": "random_repo"}}})
    )
    with pytest.raises(ValueError):
        get_config_instance(config_default_builder)


"""Start: Tests for Config.prepare_repository_configurations"""


def test_prepare_repository_configurations_auto_default() -> None:
    """Check error for prepare_repository_configurations with no default_repo."""
    from valiant.config import Config
    from valiant.repositories import RepositoryConfiguration

    default, configs = Config.prepare_repository_configurations(
        repository_configurations=[
            RepositoryConfiguration(name="test", base_url="https://www.example.com"),
        ],
        default_repository=None,
    )

    assert default == "test"


def test_multiple_repos_bad_default() -> None:
    """Check error for prepare_repository_configurations with a missing default_repo."""
    from valiant.config import Config
    from valiant.repositories import RepositoryConfiguration

    with pytest.raises(ValueError):
        Config.prepare_repository_configurations(
            repository_configurations=[
                RepositoryConfiguration(
                    name="test", base_url="https://www.example.com"
                ),
                RepositoryConfiguration(
                    name="test2", base_url="https://www.differentexample.com"
                ),
            ],
            default_repository="otter",
        )


def test_bad_config_repeated_repos() -> None:
    """Check error for prepare_repository_configurations with repeated repository entries."""
    from valiant.config import Config
    from valiant.repositories import RepositoryConfiguration

    with pytest.raises(ValueError):
        Config.prepare_repository_configurations(
            repository_configurations=[
                RepositoryConfiguration(
                    name="test", base_url="https://www.example.com"
                ),
                RepositoryConfiguration(
                    name="test", base_url="https://www.differentexample.com"
                ),
            ],
            default_repository="test",
        )


def test_multiple_repos_no_default() -> None:
    """Check error for prepare_repository_configurations with no default_repo."""
    from valiant.config import Config
    from valiant.repositories import RepositoryConfiguration

    with pytest.raises(ValueError):
        Config.prepare_repository_configurations(
            repository_configurations=[
                RepositoryConfiguration(
                    name="test", base_url="https://www.example.com"
                ),
                RepositoryConfiguration(
                    name="test2", base_url="https://www.differentexample.com"
                ),
            ],
            default_repository=None,
        )


"""End: Tests for Config.prepare_repository_configurations"""
