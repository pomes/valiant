# Introduction

Welcome!

Valiant's main purpose is to provide an auditing tool for Python-based
software development projects. The goal is to provide a tool that allows
for easy review of software dependencies and aid in determining areas of
risk for your project.

Please check out the [GitHub project site](https://github.com/pomes/valiant)
to dive into the codebase or raise/review issues.

## Features

The following Valiant functionality works towards the project goals:

- Review a Python package using the `valiant report` command
- Prepare a bill of materials for all project dependencies using the
    `valiant audit` command
- Provide a variety of reporting plugins that will help in examining dependencies
    from different angles

Valiant provides text- and JSON-based output options so the results can be either
read on-screen (command line) or provided to a reporting database. Preparing the JSON
output could be a useful part of your CI/CD process and interact with policy tools.

Be mindful that Valiant is very new and under active development. There's a lot
to be done and you must review all reports with a healthy analysis mindset.
You should also be mindful that Valiant isn't judging a project to be good or
bad - it's just trying to raise information that can help you assess risk.

## Terminology

Just so we're all on the same page:

- _Report provider_: A "plugin" that reviews the package information for items
    of interest. For example, the `safety` report provider uses the
    [safety](https://pypi.org/project/safety/) package to check for known security
    vulnerabilties.
- _Finding_: An individual item of interest determined by a report provider
- _Report_: Provides an outline of a package and combines the findings from one
    or more [report provider(s)](providers.md)
- _Audit_: Prepares a set of reports for a project's dependencies

## Quickstart

Make sure you have a Python 3.8 environment ready to go and then:

```bash
pip install valiant
valiant about
valiant report django 3.0.4
```

See the [Walkthrough](walkthrough.md) for more in-depth details.
