# SPDX License Reporting

This reporting provider matches license information in package metadata and attempts
to map it to one or more [SPDX license(s)](https://spdx.org/licenses/).

## Findings

| ID       | Title         | Discussion                              |
| -------- | ------------- | --------------------------------------- |
| SPDX001  | SPDX License found | The license could be matched to an SPDX identifier |
| SPDX002  | SPDX License not found | No match could be made |
| SPDX003  | Deprecated license | The license is marked as deprecated by SPDX |
| SPDX004  | License not OSI approved | The license meets the OSI  Open Source Definition |
| SPDX005  | License not FSF free software | The license is classified by FSF as [free](https://www.gnu.org/philosophy/free-sw.html) |

Notes:

- SPDX003, SPDX004 & SPDX005 rely on a match being found
(SPDX001).
- The provider only uses the `license` field in the package metadata and not the classifiers.

## Example

### License could not be matched

```
+----------------+---------+-------+----------+----------------+---------------+
|    Package     |   ID    | Level | Category |     Title      |    Message    |
|  Coordinates   |         |       |          |                |               |
+================+=========+=======+==========+================+===============+
| https://pypi.o | SPDX002 | info  | license  | SPDX License   | Could not map |
| rg/pypi ::     |         |       |          | not found      | licence https |
| rdflib ::      |         |       |          |                | ://raw.github |
| 4.2.2          |         |       |          |                | .com/RDFLib/r |
|                |         |       |          |                | dflib/master/ |
|                |         |       |          |                | LICENSE to an |
|                |         |       |          |                | SPDX license  |
+----------------+---------+-------+----------+----------------+---------------+
```

### License could be matched

```
+-----------------+---------+-------+----------+----------------+--------------+
|     Package     |   ID    | Level | Category |     Title      |   Message    |
|   Coordinates   |         |       |          |                |              |
+=================+=========+=======+==========+================+==============+
| https://pypi.or | SPDX001 | info  | license  | SPDX License   | BSD-3-Clause |
| g/pypi :: click |         |       |          | found          |              |
| :: 7.1.1        |         |       |          |                |              |
+-----------------+---------+-------+----------+----------------+--------------+
```

## Discussion

Python packaging can include the license information in the `license` field or as
part of a [classifier](https://pypi.org/classifiers/). The example below is a snippet
of the package metadata for the [Flask project](https://pypi.org/project/Flask/):

```json
{
    "info": {
        "classifiers": [
            "Development Status :: 5 - Production/Stable",
            "Environment :: Web Environment",
            "Framework :: Flask",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
            "Topic :: Software Development :: Libraries :: Application Frameworks",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ],
        "license": "BSD-3-Clause",
```

From the package metadata is possible to see:

1. The `"license": "BSD-3-Clause"` clause is quite specific
2. The `"License :: OSI Approved :: BSD License"` clkassifier is more general

The ["BSD License"](https://en.wikipedia.org/wiki/BSD_licenses)
could indicate one of the following license:

- [0-clause](https://opensource.org/licenses/0BSD)
- [2-clause](https://opensource.org/licenses/BSD-2-Clause)
- [3-clause](https://opensource.org/licenses/BSD-3-Clause)
- or others such as the original 4-clause

As per the
[packaging core metadata guidance](https://packaging.python.org/specifications/core-metadata/#license),
the `license` field can be used where the required license [classifer](https://pypi.org/classifiers/)
isn't available *or* to specify the license version.

SPDX includes about 17 BSD licenses in their list (!).

## Attribution

The spdx-licenses.pickle file was built from data obtained from the following URL:
https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json.
It isn't apparent what the license for the data is but other code in the GitHub Org
appears to use "Apache License 2.0"

## References

- [SPDX License List](https://spdx.org/licenses/)
- [OSI - Licenses & Standards](https://opensource.org/licenses)
- [FSF/GNU - Various Licenses and Comments about Them](https://www.gnu.org/licenses/license-list.html)
