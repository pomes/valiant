"""A centralised set of config information.

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
from .__version__ import __version__


application_name = "valiant"
application_title = "Valiant"
application_version = __version__
application_vendor = "Pomes"
application_tagline = "Dependency Investigations Unit"
application_description = "Valiant helps you investigate dependencies"
application_licence = "MIT"
application_copyright_year = 2020
application_copyright_holder = "Duncan Dickinson"
application_homepage = "https://github.com/pomes/valiant"
application_config_file = f"{application_name}.toml"
application_envvar_prefix = "VALIANT_"
pyproject_config_file = "pyproject.toml"
user_config_file = "config.toml"
