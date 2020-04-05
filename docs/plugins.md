# Plugins

_As of version 0.2.0 [Valiant report providers](providers.md) are now plugins._

Valiant uses a plugin approach based on
[Flake8's](https://flake8.pycqa.org/en/latest/plugin-development/index.html).
This allows third-parties to provide Valiant plugins that will help users in
auditing their dependencies.

## Using report plugins

You can see which report plugins are available by running `valiant config` and
check the `Loaded report plugins` line:

    Loaded report plugins: basic:0.1, demo:0.1, safety:1.8.7, localdemo:0.1, spdx:0.1

The `reports` line will tell you which reports are run by default:

    reports:  {'safety', 'basic', 'spdx'}

The default reports can be configured - see [Configuration](configuration.md).

## Write a plugin

There are two approaches to writing a plugin:

1. Using package discovery provided by Setuptools. You just need to provide one or more
    [entry points](https://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points)
    in your package.
2. Using local scripts

### Implementing

The [`demo`](https://github.com/pomes/valiant/blob/master/src/valiant/plugins/reports/demo.py)
report plugin is provided as a template from which you can build your own report plugin. The code
for `demo` is reproduced below:

```python
"""Demonstrator plugin."""
from pathlib import Path

from valiant.plugins.reports import (
    BaseReportPlugin,
    Finding,
    FindingCategory,
    FindingLevel,
    PackageMetadata,
    Report,
    get_logger,
)

log = get_logger()


class DemoReportPlugin(BaseReportPlugin):
    """A sample reporting plugin."""

    name = "demo"
    vendor = "Valiant"
    display_name = "Demo"
    version = "0.1"
    url = ""

    @classmethod
    def prepare_report(
        cls, package_metadata: PackageMetadata, configuration_dir: Path
    ) -> Report:
        """Run the report.

        Args:
            package_metadata: The package information
            configuration_dir: A directory for locating config

        Returns:
            A report with (perhaps) a finding or two.
        """
        report = Report(cls.report_provider_details())
        log.info(
            "The demo plugin was called",
            package_name=package_metadata.name,
            package_version=package_metadata.version,
        )
        report.add_finding(
            Finding(
                coordinates=package_metadata.coordinates,
                id="DEMO001",
                title="Demo finding",
                category=FindingCategory.PROJECT.value,
                level=FindingLevel.INFO,
                message="This is a demo finding",
                data={"value": "demo"},
                url="http://www.example.com",
            )
        )
        return report

```

The main work items you need to undertake are:

1. Create a class that extends `BaseReportPlugin`
2. Set your plugin class values (`name`, `version`, `vendor`, `display_name`, `url`)
3. Overload the `prepare_report` class method
4. Access your plugin either via the entry point or local approach

The `prepare_report` class method signature is as follows:

```python
@classmethod
def prepare_report(
    cls, package_metadata: PackageMetadata, configuration_dir: Path
) -> Report
```

Valiant will pass your plugin:

* An instance of
    [`PackageMetadata`](https://github.com/pomes/valiant/blob/master/src/valiant/package/model.py)
    for your plugin to report on.
* A `configuration_dir` that you might use in order to get configuration for your plugin.
    If your plugin/app has an established configuration approach you can just ignore
    `configuration_dir`.

Your implementation will work its magic and return an instance of
[`Report`](https://github.com/pomes/valiant/blob/master/src/valiant/reports/model.py)
that Valiant will add to the set of reports to be provided to the user.

Creating a report is straight-forward, just use the following:

    report = Report(cls.report_provider_details())

This will get your plugin info together (using `report_provider_details`).

From there you start adding
[`Finding`s](https://github.com/pomes/valiant/blob/master/src/valiant/reports/model.py).
A Finding is an item that your plugin determines to be a useful information item. This
could be a general bit of information, a security concern, details about project popularity
- the focus is really on anything that can help the user in auditing their dependencies.
You can take a look at the
[built-in report plugins](https://github.com/pomes/valiant/tree/master/src/valiant/plugins/reports)
to see how they're preparing findings.

Preparing a single finding is a matter of drawing together some details:

```python
report.add_finding(
    Finding(
        coordinates=package_metadata.coordinates,
        id="DEMO001",
        title="Demo finding",
        category=FindingCategory.PROJECT.value,
        level=FindingLevel.INFO,
        message="This is a demo finding",
        data={"value": "demo"},
        url="http://www.example.com",
    )
)
```

Breaking this down with some explanation:

`coordinates=package_metadata.coordinates`
:   Just use this line verbatim

`id="DEMO001"`
:   Your plugin should produce an identifier per finding type. The format for
    `id` is the uppercase name of the plugin plus a 3-digit number.

`title="Demo finding"`
:   An eye-cathing title for the finding

`category=FindingCategory.PROJECT.value`
:   An open category string. Use anything that you feel is a useful category but check the
    `FindingCategory` enum to see if one already exists.

`level=FindingLevel.INFO`
:   One of `priority`, `warning`, `info` - use the FindingLevel enum to help you.

`message="This is a demo finding"`
:   A summary of the finding.

`data={"value": "demo"}` |
:   A Mapping that provides useful data about the finding. Use JSON-convertible types
    (e.g. `str` and `int`) in the Mapping to allow for different output formats.

`url="http://www.example.com"`
:   A handy URL that will give further information about the finding.

### Entry points

As Valiant uses the [Poetry](https://python-poetry.org/) packaging tool, we can look
at its own `pyproject.toml` and see how the report plugins are flagged as entry points:

```toml
[tool.poetry.plugins."valiant.report"]
"demo" = "valiant.plugins.reports.demo:DemoReportPlugin"
"basic" = "valiant.plugins.reports.basic:BasicReportPlugin"
"spdx" = "valiant.plugins.reports.spdx:SpdxLicenseReportPlugin"
"safety" = "valiant.plugins.reports.safety:SafetyReportPlugin"
```

Valiant will look for all declared `valiant.report` entry points. Any package you've installed
(e.g. via `pip`) that declares such an entry point can then be a report provider for your
reports/audits.

### Local plugins

You don't need to package up your plugin to use it - this is handy if it's just for
a project your team is working on.

You can add the following lines to your `pyproject.toml` or any of your
[configuration files](configuration.md) to start using local plugins.

```toml
[tool.valiant.local-plugins]
paths = ["./tests/plugins"]

[tool.valiant.local-plugins."valiant.report"]
localdemo = "reports.localdemo:LocalDemoReportPlugin"
```

The `paths` item is a list of paths in which Valiant will seek out your plugin.

The `[tool.valiant.local-plugins."valiant.report"]` section contains one or more
report plugins. Each plugin is described using `<name> = "<entry point>"`.

The example above (`localdemo = "reports.localdemo:LocalDemoReportPlugin"`)
designates a report provider named `localdemo` with an entry point being a class
that extends `BaseReportPlugin`. You can review the code for this plugin at:
[LocalDemoReportPlugin](https://github.com/pomes/valiant/blob/master/tests/plugins/reports/localdemo.py)
