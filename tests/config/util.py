"""Test utilities.

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
from valiant.config import Config, ConfigBuilder

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data",)


def get_config_instance(builder: ConfigBuilder) -> Config:
    """Helper function to setup a Config instance from the builder.

    A number of builders are provided via fixtures in conftest.py

    # noqa:DAR201
    # noqa:DAR401
    """
    from valiant.config.util import ConfigMapBuilder

    conf_map = builder.build()

    if conf_map:
        return ConfigMapBuilder.generate_valiant_config_from_map(conf_map)
    else:
        raise ValueError("Failed to generate config instance.")
