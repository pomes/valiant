# Valiant and the Open Policy Agent

[Valiant](https://github.com/pomes/valiant) is an auditing tool for Python
projects. It aims to provide an easy method for gathering information about
project dependencies so as to help developers determine potential risks that
dependencies may present. Example risks include licensing issues, known
vulnerabilities and project sustainability.

The [Open Policy Agent](https://www.openpolicyagent.org/) (OPA)
provides a toolset for defining policies and comparing input data against the
policies.

In this demo I'll demonstrate how to define OPA policies and use them to review
data from Valiant. This helps determine if a project meets governance requirements.

_I'm new to OPA so please [let me know](https://github.com/pomes/valiant/issues)
if you feel the policies could be improved._

## Get started with Valiant

Valiant is a Python package available on [PyPi](https://pypi.org/project/valiant/).

Installing Valiant requires Python 3.8 and the standard `pip` command:

    pip install -U valiant

Once installed, check the details with:

    valiant about

Version 0.2.1 or above will be fine for this article.

Say you wanted to check the details for the
[Flask package](https://pypi.org/project/Flask/):

    valiant report flask 1.1.1

That displays a human-readable output but for OPA we'll need JSON:

    valiant report flask 1.1.1 -o json

It's more likely that you'll want to check all of a project's dependencies
against your policies. I'll use [Poetry](https://python-poetry.org/) to initialise
a project and add some dependencies:

```bash
pip install poetry
poetry new demo_project
cd demo_project
poetry add flask==1.1.1
poetry add insecure-package==0.1.0
```

You'll be able to see the project configuration in the
[`pyproject.toml`](opa/pyproject.toml) file.
To see the non-development dependencies, try `poetry show --no-dev`. For
a nice tree view, try `poetry show --no-dev --tree` and you'll get something
similar to the output below:

```
flask 1.1.1 A simple framework for building complex web applications.
├── click >=5.1
├── itsdangerous >=0.24
├── jinja2 >=2.10.1
│   └── markupsafe >=0.23
└── werkzeug >=0.15
insecure-package 0.1.0 Insecure Package, don't use it
```

_The `insecure-package` is a demo package that the
[safety scanner](https://pypi.org/project/safety/) uses as a demonstrator package -
it is safe to use._

Now that we have a (small) project set up, we can run Valiant reporting for the dependencies:

```bash
# Export the dependencies to a requirements.txt file:
poetry export --format requirements.txt --output requirements.txt --without-hashes

# Display a list of findings
poetry run valiant audit requirements.txt -s
```

The output will be a table of findings similar to the one below:

```
+--------------+-----------+----------+----------+--------------+--------------+
|   Package    |    ID     |  Level   | Category |    Title     |   Message    |
| Coordinates  |           |          |          |              |              |
+==============+===========+==========+==========+==============+==============+
| https://pypi | SPDX001   | info     | license  | SPDX License | BSD-3-Clause |
| .org/pypi :: |           |          |          | found        |              |
| click ::     |           |          |          |              |              |
| 7.1.2        |           |          |          |              |              |
+--------------+-----------+----------+----------+--------------+--------------+
| https://pypi | SPDX001   | info     | license  | SPDX License | BSD-3-Clause |
| .org/pypi :: |           |          |          | found        |              |
| Flask ::     |           |          |          |              |              |
| 1.1.1        |           |          |          |              |              |
+--------------+-----------+----------+----------+--------------+--------------+
| https://pypi | BASIC003  | warning  | project  | No link to   | The project  |
| .org/pypi :: |           |          |          | codebase     | doesn't      |
| insecure-    |           |          |          |              | provide a    |
| package ::   |           |          |          |              | link to its  |
| 0.1.0        |           |          |          |              | codebase.    |
+--------------+-----------+----------+----------+--------------+--------------+
```

Whilst a table is handy for us to read, we'll need JSON to feed into OPA:

```
# Audit the requirements with JSON output:
valiant audit requirements.txt --out json>valiant_audit.json
```

_Hint: use the [`jq`](https://stedolan.github.io/jq/) tool to view the audit data:
`cat valiant_audit.json |jq`_

You can find a copy of the audit output in the project repository
under [`docs/demo/opa/valiant_audit.json`](opa/valiant_audit.json).

Now that we have the basics of Valiant sorted out, let's take OPA for a quick spin.

## Get started with OPA

Through this article I'll use a [local copy of OPA](https://www.openpolicyagent.org/docs/latest/#1-download-opa).

You could also use an [OPA docker image](https://hub.docker.com/r/openpolicyagent/opa):

    docker pull docker.io/openpolicyagent/opa

The code for used in this article is located in the
[`docs/demo/opa`](https://github.com/pomes/valiant/tree/master/docs/demo/opa)
directory of the [Valiant GitHub project](https://github.com/pomes/valiant).
I'll provide most of the code in this article so you don't need to get a copy
of the repository (but you're always welcome to do so).

The [Rego playground](https://play.openpolicyagent.org) is a useful
tool for trying out policy files. You can copy the `.rego` code from this article
and try it out in the playground.

The [OPA extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=tsandall.opa)
is worth trying out if you're using VSCode.

### A basic policy test

OPA policies are defined in a `rego` file. The code below defines a policy that requires
that an MIT license be used:

_basic.rego:_
```
package basic

default allow = false

allow {
    input.license == "MIT"
}
```

[Policy testing](https://www.openpolicyagent.org/docs/latest/policy-testing/)
provides a mechanism for checking that the policy is capturing conditions
correctly. The code below provides a basic test suite for our basic policy:

_basic_test.rego:_
```
package basic

test_app_allowed {
    allow with input as {"name": "valiant", "license": "MIT"}
}

test_app_not_allowed {
    not allow with input as {"name": "my_app", "license": "BSD-3-Clause"}
}

test_app_not_allowed_missing_license {
    not allow with input as {"name": "my_app"}
}
```

Let's run the tests:

    ./opa test basic -v

The output should appear as follows:

```
data.basic.test_app_allowed: PASS (127.108075ms)
data.basic.test_app_not_allowed: PASS (429.647µs)
data.basic.test_app_not_allowed_missing_license: PASS (421.856µs)
--------------------------------------------------------------------------------
PASS: 3/3
```

Consider an input that provides the correct license:

```json
{
    "name": "test",
    "license": "MIT"
}
```

We can check this against the policy using:

    ./opa eval \
        --data basic/basic.rego \
        --input input/input_1.json  \
        --format pretty \
        'data.basic'

The result indicates that the input meets the policy requirement:

```json
{
  "allow": true
}
```

A different input uses an unacceptable license:

```json
{
    "name": "test2",
    "license": "Commercial"
}

```

Running an evaluation against the input:

    ./opa eval \
        --data basic/basic.rego \
        --input input/input_2.json  \
        --format pretty \
        'data.basic'

... and we see that `false` is returned and the policy is not met:

```json
{
  "allow": false
}
```

## Test a single package

Let's move on and start using real data. This time we want to check if a
candidate dependency will meet policy requirements.

First of all, produce Valiant reports for a number of packages:

```bash
valiant report flask 1.1.1 --out json > report/flask.json
valiant report django 1.2 --out json > report/django.json
valiant report valiant 0.2.1 --out json > report/valiant.json
```

_Note: I've used a very old version of Django so as to illustrate security findings._

Valiant uses reporting plugins to produce a set of _findings_ for each package.
You can quickly view these with `valiant report django 1.2 -s` or, with the json
we produced just before, you can create a summary with:

    cat report/valiant.json \
        | jq '.reports[].findings[] | {id:.id, package: .coordinates.name, version: .coordinates.version, title: .title, message: .message, data: .data}'

So now we have some input data to test, let's create some policies.

_The [`policies/dependency.rego`](opa/policies/dependency.rego) file contains
all of the policies discussed in this section._

First of all, I want to make sure I'm only using packages with a correctly declared
licence. The [Valiant SPDC reporting plugin](https://github.com/pomes/valiant/blob/master/src/valiant/plugins/reports/spdx/README.md)
returns the `SPDX002` finding when the package's licence could not be determined.
The check below will note a violation on an `SPDX002` finding:

```bash
violations[pkg] = message {
    # All packages must have a properly declared license
    findings := input.reports.spdx.findings[_]
    findings.id == "SPDX002"
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := "SPDX002: No licence could be determined."
}
```

Next, I want to make sure that, where a license could be determined (`SPDX001`), it is
an [OSI approved license](https://opensource.org/licenses/alphabetical).
The following policy will check that a license was found and it is an OSI approved license:

```bash
violations[pkg] = message {
    # All packages must have an OSI-approved license
    findings := input.reports.spdx.findings[_]
    findings.id == "SPDX001"; findings.data.is_osi_approved != true
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := "An OSI-approved licence is required."
}
```

Valiant's [Safety report provider](https://github.com/pomes/valiant/blob/master/src/valiant/plugins/reports/safety/README.md)
uses the [Safety package](https://pypi.org/project/safety/) to determine any known vulnerabilities
for a package. This check just looks for any `SAFETY001` findings:

```bash
violations[pkg] = message  {
    # Any findings from the safety report needs to be raised
    findings := input.reports.safety.findings[_]
    findings.id == "SAFETY001"
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := concat(": ", [findings.id, findings.message])
}
```

Finally I want to check for packages that the
[Basic report provider](https://github.com/pomes/valiant/tree/master/src/valiant/plugins/reports/basic)
determines as not production ready. The `BASIC005` finding flags packages with a development
status between 1 and 4 (refer to the [classifiers](https://pypi.org/classifiers/)) and `BASIC006`
flags packages marked as inactive.

```bash
violations[pkg] = message {
    # Packages not marked as production-ready
    not_mature := {"BASIC005", "BASIC006"}
    findings := input.reports.basic.findings[_]
    not_mature[findings.id]
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := concat(": ", [findings.id, findings.message])
}
```

The `allow` rule will return `true` if no violations were found:

```bash
allow = true {
    count(violations) == 0
}
```

### Policy check

We can check the Flask report from Valiant against the policy:

    ./opa eval --data policies \
               --input report/flask.json \
               --format pretty \
               'data.valiant.demo.dependency.allow'

The output is `true`, indicating that the `allow` policy was met. That's handy
for a visual check but OPA can give us something a bit more tangible:

    ./opa eval --data policies \
               --input report/flask.json \
               --format pretty \
               --fail-defined 'data.valiant.demo.dependency.violations[pkg]'

The resulting output of `undefined` indicates that there were no violations.
By using the `--fail-defined` parameter, the exit code is set based on if any
result was found. Calling `echo $?` displays `0`, indicating that the `flask.json`
data does not raise any policy violations.

Trying the evaluation against the `valiant.json` report will yield a policy violation:

```bash
./opa eval --data policies \
           --input report/valiant.json \
           --format pretty \
           --fail-defined 'data.valiant.demo.dependency.violations[pkg]'
echo $?
```

The exit value (`$?`) of `1` indicates that there were violations and the
table displayed by OPA describes the issue:

```
+------------------+----------------------------------------------+
|       pkg        | data.valiant.demo.dependency.violations[pkg] |
+------------------+----------------------------------------------+
| "valiant::0.2.1" | "BASIC005: The package is                    |
|                  | marked as '1 - Planning'"                    |
+------------------+----------------------------------------------+
```

The report from the very old Django version will yield even more to be
concerned about:

```
./opa eval --data policies \
           --input report/django.json \
           --format pretty \
           --fail-defined 'data.valiant.demo.dependency.violations[pkg]'
```

There are a lot of violations coming from that report! Here's an excerpt:

```
+---------------+----------------------------------------------+
|      pkg      | data.valiant.demo.dependency.violations[pkg] |
+---------------+----------------------------------------------+
| "Django::1.2" | "SPDX002: No licence could be                |
|               | determined."                                 |
| "Django::1.2" | "SAFETY001: Django before                    |
|               | 1.11.27, 2.x before 2.2.9,                   |
|               | and 3.x before 3.0.1 allows                  |
|               | account takeover. A suitably                 |
|               | crafted email address (that                  |
|               | is equal to an existing user's               |
|               | email address after case                     |
|               | transformation of Unicode                    |
|               | characters) would allow an                   |
|               | attacker to be sent a password               |
|               | reset token for the matched                  |
|               | user account. (One mitigation                |
|               | in the new releases is to send               |
|               | password reset tokens only                   |
|               | to the registered user email                 |
|               | address.) See CVE-2019-19844."               |
| "Django::1.2" | "SAFETY001: Cross-site                       |
|               | scripting (XSS) vulnerability                |
|               | in Django 1.2.x before 1.2.2                 |
|               | allows remote attackers to                   |
|               | inject arbitrary web script or               |
|               | HTML via a csrfmiddlewaretoken               |
|               | (aka csrf_token) cookie."                    |
```

## Auditing a project

It's more likely that we'll want to check the full set of project dependencies against
our policies. This would be handy as part of a CI/CD pipeline as we could block non-compliant
projects from being deployed.

Recall that earlier I used `poetry` to generate the dependency list and passed this
to `valiant` produce an audit report:

```bash
# Export the dependencies to a requirements.txt file:
poetry export --format requirements.txt --output requirements.txt --without-hashes

# Run an audit and output JSON:
valiant audit requirements.txt --out json>valiant_audit.json
```

The resulting JSON is an array of reports (1 per package) and each report will have
0 or more findings garnered from the various reporting plugins we've used. This is
a different structure to the single-package report covered in the last section so
the policies will need some changes.

The [`audit-policies/main.rego`](audit-policies/main.rego) policy file defines a
suite of checks to determine aspects of the Valiant audit report that breach policy.
It's quite similar to the policy described earlier - just with some slightly different
checks:

```bash
package valiant.demo

default allow = false

violations[pkg] = message {
    # Packages not marked as production-ready
    not_mature := {"BASIC005", "BASIC006"}
    findings := input[_].reports.basic.findings[_]
    not_mature[findings.id]
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := concat(": ", [findings.id, findings.message])
}

violations[pkg] = message {
    # Only allow specifically approved licences
    permitted_licenses := {"BSD-3-Clause", "MIT"}
    findings := input[_].reports.spdx.findings[_]
    findings.id == "SPDX001"
    not permitted_licenses[findings.message]
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := concat(": ", [findings.id, findings.message])
}

violations[pkg] = message {
    # All packages must have a properly declared license
    findings := input[_].reports.spdx.findings[_]
    findings.id == "SPDX002"
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := concat(": ", [findings.id, findings.message])
}

violations[pkg] = message  {
    # Any findings from the safety report needs to be raised
    findings := input[_].reports.safety.findings[_]
    findings.id == "SAFETY001"
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := concat(": ", [findings.id, findings.message])
}

allow = true {
    count(violations) == 0
}
```

_Note: a small test suite is provided and can be run with `./opa test policies -v`._

### Policy check

Now that we have the policy defined and the input data ready, we can perform an evaluation:

```
./opa eval --data policies/ \
           --input valiant_audit.json \
           --format pretty \
           --fail-defined 'data.valiant.demo.audit.violations[pkg]'
```

```
+---------------------------+-----------------------------------+
|            pkg            | data.valiant.demo.violations[pkg] |
+---------------------------+-----------------------------------+
| "insecure-package::0.1.0" | "BASIC005: The package is         |
|                           | marked as '2 - Pre-Alpha'"        |
| "insecure-package::0.1.0" | "SPDX002: Could not map           |
|                           | licence MIT license to an SPDX    |
|                           | license"                          |
| "itsdangerous::1.1.0"     | "SPDX002: Could not map           |
|                           | licence BSD to an SPDX            |
|                           | license"                          |
| "insecure-package::0.1.0" | "SAFETY001: This is an            |
|                           | insecure package with lots        |
|                           | of exploitable security           |
|                           | vulnerabilities."                 |
+---------------------------+-----------------------------------+
```

As an aside, you may note that `insecure-package` is reported as not having an SPDX licence.
Whilst the Pypi metadata for the package does provide `"license": "MIT license"`, the reporting
just looks for `MIT` and it's the additional ` license` that causes a failed match. Perhaps
as Valiant matures this matching will improve.

Again, by using the `--fail-defined 'data.valiant.demo.violations[pkg]'` parameter we can then check
the exit code (`echo $?`) and see the command returned `1`. The policy
check could be wrapped in a script or some other construct in a continuous integration process
that causes the build to fail. Using this approach provides an easy policy layer to the CI/CD
process and can prevent deployments that don't meet policy guidelines.

## Conclusion

This article has outlined a method for defining policies for a project and using
Valiant to supply data for policy validation. This light-weight process can be
used by a developer as part of their daily routine and pre-commit checks.

In a broader usage model, OPA could be
[run as a central policy server](https://www.openpolicyagent.org/docs/latest/#4-try-opa-run-server)
and used by CI/CD pipelines to ensure that only compliant codebases are able to be
deployed.

The Valiant project is very young but it [supports plugins](../plugins.md) for gathering information
about Python dependencies. You can readily add reports that run under Valiant and
then check that (meta)data using OPA.

Ultimately, the goal is to recognise/reduce risk in your software project's supply chain.
This contributes to teams ensuring sustainability in their projects.

## Further reading:

- [OPA Documentation](https://www.openpolicyagent.org/docs/latest/)
- [Policy-driven continuous integration with Open Policy Agent](https://blog.openpolicyagent.org/policy-driven-continuous-integration-with-open-policy-agent-b98a8748e536)
- [Kubernetes Podcast: Open Policy Agent, with Tim Hinrichs and Torin Sandall](https://kubernetespodcast.com/episode/101-open-policy-agent/)
