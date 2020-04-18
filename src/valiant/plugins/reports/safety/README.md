# Safety report provider

This plugin is a wrapper for the
[Safety package](https://pypi.org/project/safety/) and
checks if a package has a known vulnerability.

## Findings

| ID       | Title         | Discussion                              |
| -------- | ------------- | --------------------------------------- |
| SAFETY001 | Vulnerability found | Safety determined that a vulnerability was found for this package |

## Example

```
+--------------+-----------+----------+----------+--------------+--------------+
|   Package    |    ID     |  Level   | Category |    Title     |   Message    |
| Coordinates  |           |          |          |              |              |
+==============+===========+==========+==========+==============+==============+
| https://pypi | SAFETY001 | priority | security | Vulnerabilit | The CLI      |
| .org/pypi :: |           |          |          | y found      | tools in     |
| rdflib ::    |           |          |          |              | RDFLib 4.2.2 |
| 4.2.2        |           |          |          |              | can load     |
|              |           |          |          |              | Python       |
|              |           |          |          |              | modules from |
|              |           |          |          |              | the current  |
|              |           |          |          |              | working      |
|              |           |          |          |              | directory,   |
|              |           |          |          |              | allowing     |
|              |           |          |          |              | code         |
|              |           |          |          |              | injection,   |
|              |           |          |          |              | because      |
|              |           |          |          |              | "python -m"  |
|              |           |          |          |              | looks in     |
|              |           |          |          |              | this         |
|              |           |          |          |              | directory,   |
|              |           |          |          |              | as           |
|              |           |          |          |              | demonstrated |
|              |           |          |          |              | by rdf2dot.  |
+--------------+-----------+----------+----------+--------------+--------------+
```

## Configuration

* Use the `SAFETY_API_KEY` environment variable to provide a pyup key.
* A comma-separated list in the `SAFETY_IGNORE_IDS` environment variable is
    used to ignore vulnerabilities by ID.

Please refer to the [Safety website](https://pyup.io/safety/) for details.

## Discussion

None.

## References

- [Safety website](https://pyup.io/safety/)
