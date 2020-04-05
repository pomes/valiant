# Basic report provider

Reviews the package information to determine if:

- key metadata fields are provided
- the package artifacts (downloads) were signed
- the package is marked as production-ready

## Findings

| ID       | Title         | Discussion                              |
| -------- | ------------- | --------------------------------------- |
| BASIC001 | No license found | The `license` field was not provided |
| BASIC002 | No link to project site | A link wasn't provided in the `home_page` or `project_url` fields or under `Homepage` in the `project_urls` dictionary |
| BASIC003 | No link to codebase | A link wasn't provided under `Code` in the `project_urls` dictionary |
| BASIC004 | An artifact has not been signed | An artifact (download) such as the `Wheel` or `Source` file was not signed by the provider |
| BASIC005 | Package not production ready | The package classifiers do not include `Development Status :: 5 - Production/Stable` or `Development Status :: 6 - Mature` |
| BASIC006 | Package is marked as inactive | The package classifiers includes `Development Status :: 7 - Inactive`|

## Configuration

None

## Discussion

It's important that key metadata fields are provided by the package
author as they clarify aspects such as the license and useful resources (e.g. the project and code sites).

The package classifiers provide the `Development Status` category
and this should indicate the level to which a downstream project
can rely on the package in a production setting.

Signing packages is a useful idea as it provides some level of
assurance regarding who created the package. It is not, however
a black and white finding. Repositories such as PyPi will allow
you to download the `.asc` file for an artifact but you are still
left with key questions:

1. Do I trust the key?
1. Who is the key owner?
1. Do I trust the key owner?

Remember that anyone can create a key and sign something. They can
even publish their key information but that doesn't mean you
know/trust them.

## References

- [Python Packaging - Core metadata specifications](https://packaging.python.org/specifications/core-metadata/)
- [PyPi Classifiers](https://pypi.org/classifiers/)
- The [twine](https://github.com/pypa/twine#why-should-i-use-this)
    documentation describes artifact signing
