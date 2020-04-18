"""Valiant Config tests.

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

"""
Valiant builds up configuration using a base configuration followed
by a series of overlaying sources. The approach is described in
docs/configuration.md.

The valiant.console.commands.base_command.singleton_valiant() method
demonstrates how a Valiant configuration is brought together:


    config_builder = create_valiant_builder()
    if command.option("config"):
        config_builder.add_source(
            TomlSource(Path(command.option("config")), optional=False)
        )
    conf_map = config_builder.build()


It is important that the tests provided here take into account the overlay
approach and that the correct config setting is being used.

* test_basics.py primarily check that the data model basics are sound

* test_config_default.py tests that the default configuration provides the
    expected base config

* test_config_overlay_file.py tests that the expected configuration is in use
    after one or more configuration files are loaded

* test_valiant_config.py tests Valiant config by loading various overlay files.

A set of test configuration files is provided in the data/ dir.

The test_test_setup.py file just checks that the fixtures are working as expected.

Note that override_appdirs in tests/conftest.py patches the directories provided
by AppDirs

"""
