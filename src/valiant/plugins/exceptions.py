"""Plugin-centric exceptions.

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
import sys

from importlib.metadata import EntryPoint

from valiant.exceptions import ValiantException


class FailedToLoadPlugin(ValiantException):  # noqa: D101
    def __init__(
        self,
        exception: Exception,
        plugin_name: str = None,
        entry_point: EntryPoint = None,
    ):  # noqa: DAR101
        """Initialize FailedToLoadPlugin exception."""
        self.plugin_name = plugin_name
        self.original_exception = exception
        self.entry_point = entry_point

    def __str__(self):  # type: () -> str
        """Format our exception message."""  # noqa: DAR201
        return (
            f"Failed to load plugin '{self.plugin_name}' due to {self.original_exception}. "
            f"Entry point is: {self.entry_point}. "
            f"sys.path is: {sys.path}"
        )
