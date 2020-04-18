"""Validation dictionary.

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
The hideous construct below provides a list of tuples.

Each tuple contains the following:

1. A filename for a json file located in the 'package-data' directory.
    These are taken from actual PyPi projects.

2. A Dictionary that maps a subset (or all) of the expected data

This setup lets us parametrize a set of test inputs and assert against the
expected values. The code below indicates how to apply this to a test:

    @pytest.mark.parametrize(
        ("input_file,expected"), DATAFILE_VALIDATION,
    )

"""
DATAFILE_VALIDATION = [
    (
        "flask-1.1.1.json",
        {
            "name": "Flask",
            "version": "1.1.1",
            "license": "BSD-3-Clause",
            "url_code": "https://github.com/pallets/flask",
            "url_documentation": "https://flask.palletsprojects.com/",
            "url_project": "https://palletsprojects.com/p/flask/",
            "url_issue_tracker": "https://github.com/pallets/flask/issues",
            "requires_python": [
                ">=2.7",
                "!=3.0.*",
                "!=3.1.*",
                "!=3.2.*",
                "!=3.3.*",
                "!=3.4.*",
            ],
            "requires_dist": {
                "Werkzeug": [
                    {
                        "name": "Werkzeug",
                        "url": None,
                        "specifiers": [
                            {"version": "0.15", "operator": ">=", "prereleases": False}
                        ],
                        "extras": [],
                        "marker": None,
                    }
                ],
                "pallets-sphinx-themes": [
                    {
                        "name": "pallets-sphinx-themes",
                        "url": None,
                        "specifiers": [],
                        "extras": [],
                        "marker": 'extra == "dev"',
                    },
                    {
                        "name": "pallets-sphinx-themes",
                        "url": None,
                        "specifiers": [],
                        "extras": [],
                        "marker": 'extra == "docs"',
                    },
                ],
            },
        },
    )
]
