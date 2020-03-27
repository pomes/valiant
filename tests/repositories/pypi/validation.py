"""Validation dictionary.

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
