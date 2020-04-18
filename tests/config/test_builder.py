"""Tests ConfigBuilder basic functionality.

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


def test_empty_builder() -> None:
    """Test that a builder with no sources returns None at build time."""
    from valiant.config import ConfigBuilder

    builder = ConfigBuilder()

    c = builder.build()

    # Nothing was processed so we get None
    assert not c


def test_basic_build_with_single_mapping_source() -> None:
    """Basic test that a source config is reflected in a build."""
    from valiant.config import ConfigBuilder
    from valiant.config.source import MappingSource

    builder = ConfigBuilder()
    builder.add_source(MappingSource({"name": "Fred"}))
    c = builder.build()
    assert c
    assert c["name"] == "Fred"
    assert c["_builder_metadata"]["build_results"]["dictionary"] == "Read"


def test_basic_build_with_two_mapping_sources() -> None:
    """Check that a second source overlays a value."""
    from valiant.config import ConfigBuilder
    from valiant.config.source import MappingSource

    builder = ConfigBuilder()
    builder.add_source(MappingSource({"name": "Fred"}))
    builder.add_source(MappingSource({"name": "Jane"}))
    c = builder.build()
    assert c
    assert c["name"] == "Jane"
    # The dictionary read is recorded only once
    assert c["_builder_metadata"]["build_results"]["dictionary"] == "Read"


def test_basic_build_with_two_mapping_sources_that_are_filtered_out() -> None:
    """Test handling of a filter that throws everything away."""
    from valiant.config import ConfigBuilder
    from valiant.config.source import MappingSource

    builder = ConfigBuilder(filter=lambda d: {})
    assert builder

    builder.add_source(MappingSource({"name": "Fred"}))
    builder.add_source(MappingSource({"name": "Jane"}))
    c = builder.build()

    assert c
    assert "name" not in c
    assert c["_builder_metadata"]["build_results"]["dictionary"] == "Read"


def test_basic_build_with_two_mapping_sources_with_object() -> None:
    """Check that a second source overlays a value."""
    from valiant.config import ConfigBuilder
    from valiant.config.source import MappingSource

    builder = ConfigBuilder()
    builder.add_source(
        MappingSource({"name": "Fred", "pets": {"fido": "dog", "mittens": "cat"}})
    )
    builder.add_source(MappingSource({"name": "Jane", "pets": {"flipper": "fish"}}))
    builder.add_source(MappingSource({"name": "Dewi"}))
    c = builder.build()
    assert c
    assert c["name"] == "Dewi"
    assert c["pets"]["flipper"] == "fish"
    assert "fido" not in c["pets"]
    assert "mittens" not in c["pets"]
    # The dictionary read is recorded only once
    assert c["_builder_metadata"]["build_results"]["dictionary"] == "Read"


def test_default_builder_with_no_sources() -> None:
    """Expect that the default builder doesn't build anything without inputs."""
    from valiant.config import ConfigBuilder

    builder = ConfigBuilder.create_default_builder(
        include_pyproject=False, include_user_config=False, include_site_config=False
    )
    assert not builder.build()
