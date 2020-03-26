# Walkthrough

Before you start, please remember that Valiant is brand new and still in
a state of change/development. You should make sure that you use Valiant
with this is mind.

## Install

You need to be running Python 3.8 or higher. If you're not running 3.8,
[pyenv](https://github.com/pyenv/pyenv) can make this very easy for you
and I'd strongly recommend checking out their instructions.

I'd also recommend using a virtual environment. The "built in" approach to
this (once you have Python 3.8 installed) is to:

    python -m virtualenv --python 3.8 venv
    . venv/bin/activate
    python --version

Hopefully you get something like `Python 3.8.x`. With that going you can now
install Valiant:

    pip install valiant

...and check it's working:

    valiant about

### Containers

Containers can be handy if you're just taking Valiant for a spin.

Grab a copy of the Python 3.8 image:

    docker pull docker.io/python:3.8

Start it up:

    docker run --rm -it docker.io/python:3.8 /bin/bash

Once in the container shell you can install Valiant and try it out:

    pip install valiant
    valiant about


### From the GitHub project

    pip install git+https://github.com/pomes/valiant.git


It's a really good idea to do this type of thing in a virtual env!
Poetry will help you out here and install Valiant as a dev dependency:

```bash
poetry add -D git+https://github.com/pomes/valiant.git
```

## Configuration

It's still very early days and Valiant isn't configurable. You can check the
settings with:

    valiant config

This will display the current configuration:

    cache_dir: /home/fred/.cache/valiant/0.1.0
    config_dir: /home/fred/.config/valiant/0.1.0
    default_repository_name: pypi
    repositories: pypi
    reports: basic,spdx,safety

If you check the `config_dir` you'll see that Valiant is putting its logs in there.

You'll also notice that wherever you run the `valiant` command you'll see a file named
`valiant-0.1.0-requests-cache.sqlite` has been created. This is a cache for web
requests and helps both speed up Valiant as well as reduce load on repository servers.
Track any update to this in [Issue #4](https://github.com/pomes/valiant/issues/4).

## Review a dependency

Say you wanted to find out about a dependency. The `report` command will give
you information about the project/release plus run some checks.

Let's try it out:

```bash
valiant report flask 1.1.1
```

You'll get the following output:

```
Package metadata
+-------------+----------------------------------------------------------------+
|    Item     |                            Value(s)                            |
+=============+================================================================+
| Package     | Flask                                                          |
+-------------+----------------------------------------------------------------+
| Version     | 1.1.1                                                          |
+-------------+----------------------------------------------------------------+
| Repository  | https://pypi.org/pypi                                          |
+-------------+----------------------------------------------------------------+
| License     | BSD-3-Clause                                                   |
+-------------+----------------------------------------------------------------+
| Summary     | A simple framework for building complex web applications.      |
+-------------+----------------------------------------------------------------+
| Resources   | Project: https://palletsprojects.com/p/flask/                  |
|             | Code: https://github.com/pallets/flask                         |
|             | Documentation: https://flask.palletsprojects.com/              |
|             | Issue tracker:: https://github.com/pallets/flask/issues        |
+-------------+----------------------------------------------------------------+
| Classifiers | Development Status :: 5 - Production/Stable                    |
|             | Environment :: Web Environment                                 |
|             | Framework :: Flask                                             |
|             | Intended Audience :: Developers                                |
|             | License :: OSI Approved :: BSD License                         |
|             | Operating System :: OS Independent                             |
|             | Programming Language :: Python                                 |
|             | Programming Language :: Python :: 2                            |
|             | Programming Language :: Python :: 2.7                          |
|             | Programming Language :: Python :: 3                            |
|             | Programming Language :: Python :: 3.5                          |
|             | Programming Language :: Python :: 3.6                          |
|             | Programming Language :: Python :: 3.7                          |
|             | Topic :: Internet :: WWW/HTTP :: Dynamic Content               |
|             | Topic :: Internet :: WWW/HTTP :: WSGI :: Application           |
|             | Topic :: Software Development :: Libraries :: Application      |
|             | Frameworks                                                     |
|             | Topic :: Software Development :: Libraries :: Python Modules   |
+-------------+----------------------------------------------------------------+
| Artifacts   | bdist_wheel: https://files.pythonhosted.org/packages/9b/93/628 |
|             | 509b8d5dc749656a9641f4caf13540e2cdec85276964ff8f43bbb1d3b/Flas |
|             | k-1.1.1-py2.py3-none-any.whl                                   |
|             | ---                                                            |
|             | sdist: https://files.pythonhosted.org/packages/2e/80/3726a729d |
|             | e758513fd3dbc64e93098eb009c49305a97c6751de55b20b694/Flask-1.1. |
|             | 1.tar.gz                                                       |
+-------------+----------------------------------------------------------------+

Report: Basic [https://pypi.org/pypi :: Flask :: 1.1.1]
No findings

Report: SPDX License [https://pypi.org/pypi :: Flask :: 1.1.1]
+----------+---------+----------+--------------------+--------------+
| Priority |   ID    | Category |       Title        |   Message    |
+==========+=========+==========+====================+==============+
|   info   | SPDX001 | license  | SPDX License found | BSD-3-Clause |
+----------+---------+----------+--------------------+--------------+

Report: Safety [https://pypi.org/pypi :: Flask :: 1.1.1]
No findings
```

It all looks pretty good. Let's try another one:

```bash
valiant report rdflib 4.2.2
```

This will yield some findings for us to consider:

```
Package metadata
+-------------+----------------------------------------------------------------+
|    Item     |                            Value(s)                            |
+=============+================================================================+
| Package     | rdflib                                                         |
+-------------+----------------------------------------------------------------+
| Version     | 4.2.2                                                          |
+-------------+----------------------------------------------------------------+
| Repository  | https://pypi.org/pypi                                          |
+-------------+----------------------------------------------------------------+
| License     | https://raw.github.com/RDFLib/rdflib/master/LICENSE            |
+-------------+----------------------------------------------------------------+
| Summary     | RDFLib is a Python library for working with RDF, a simple yet  |
|             | powerful language for representing information.                |
+-------------+----------------------------------------------------------------+
| Resources   | Project: https://github.com/RDFLib/rdflib                      |
|             | Code:                                                          |
|             | Documentation:                                                 |
|             | Issue tracker::                                                |
+-------------+----------------------------------------------------------------+
| Classifiers | License :: OSI Approved :: BSD License                         |
|             | Natural Language :: English                                    |
|             | Operating System :: OS Independent                             |
|             | Programming Language :: Python                                 |
|             | Programming Language :: Python :: 2                            |
|             | Programming Language :: Python :: 2.6                          |
|             | Programming Language :: Python :: 2.7                          |
|             | Programming Language :: Python :: 3                            |
|             | Programming Language :: Python :: 3.3                          |
|             | Programming Language :: Python :: 3.4                          |
|             | Programming Language :: Python :: 3.5                          |
|             | Topic :: Software Development :: Libraries :: Python Modules   |
+-------------+----------------------------------------------------------------+
| Artifacts   | bdist_wheel: https://files.pythonhosted.org/packages/3c/fe/630 |
|             | bacb652680f6d481b9febbb3e2c3869194a1a5fc3401a4a41195a2f8f/rdfl |
|             | ib-4.2.2-py3-none-any.whl                                      |
|             | ---                                                            |
|             | sdist: https://files.pythonhosted.org/packages/c5/77/1fa0f4cff |
|             | d5faad496b1344ab665902bb2609f56e0fb19bcf80cff485da0/rdflib-4.2 |
|             | .2.tar.gz                                                      |
+-------------+----------------------------------------------------------------+

Report: Basic [https://pypi.org/pypi :: rdflib :: 4.2.2]
+----------+----------+----------+----------------------+----------------------+
| Priority |    ID    | Category |        Title         |       Message        |
+==========+==========+==========+======================+======================+
| warning  | BASIC003 | project  | No link to codebase  | The project doesn't  |
|          |          |          |                      | provide a link to    |
|          |          |          |                      | its codebase.        |
+----------+----------+----------+----------------------+----------------------+
| warning  | BASIC004 | project  | An artifact has not  | A package of type    |
|          |          |          | been signed          | bdist_wheel has not  |
|          |          |          |                      | been signed          |
+----------+----------+----------+----------------------+----------------------+
| warning  | BASIC004 | project  | An artifact has not  | A package of type    |
|          |          |          | been signed          | sdist has not been   |
|          |          |          |                      | signed               |
+----------+----------+----------+----------------------+----------------------+

Report: SPDX License [https://pypi.org/pypi :: rdflib :: 4.2.2]
+----------+---------+----------+-----------------------+----------------------+
| Priority |   ID    | Category |         Title         |       Message        |
+==========+=========+==========+=======================+======================+
|   info   | SPDX002 | license  | SPDX License not      | Could not map        |
|          |         |          | found                 | licence https://raw. |
|          |         |          |                       | github.com/RDFLib/rd |
|          |         |          |                       | flib/master/LICENSE  |
|          |         |          |                       | to an SPDX license   |
+----------+---------+----------+-----------------------+----------------------+

Report: Safety [https://pypi.org/pypi :: rdflib :: 4.2.2]
+----------+-----------+----------+---------------------+----------------------+
| Priority |    ID     | Category |        Title        |       Message        |
+==========+===========+==========+=====================+======================+
| priority | SAFETY001 | security | Vulnerability found | The CLI tools in     |
|          |           |          |                     | RDFLib 4.2.2 can     |
|          |           |          |                     | load Python modules  |
|          |           |          |                     | from the current     |
|          |           |          |                     | working directory,   |
|          |           |          |                     | allowing code        |
|          |           |          |                     | injection, because   |
|          |           |          |                     | "python -m" looks in |
|          |           |          |                     | this directory, as   |
|          |           |          |                     | demonstrated by      |
|          |           |          |                     | rdf2dot.             |
+----------+-----------+----------+---------------------+----------------------+
```

Sometimes you just want the findings:

```bash
valiant report rdflib 4.2.2 -s
```

This will give us a quick table to check:

```
+--------------+-----------+----------+----------+--------------+--------------+
|   Package    |    ID     |  Level   | Category |    Title     |   Message    |
| Coordinates  |           |          |          |              |              |
+==============+===========+==========+==========+==============+==============+
| https://pypi | BASIC003  | warning  | project  | No link to   | The project  |
| .org/pypi :: |           |          |          | codebase     | doesn't      |
| rdflib ::    |           |          |          |              | provide a    |
| 4.2.2        |           |          |          |              | link to its  |
|              |           |          |          |              | codebase.    |
+--------------+-----------+----------+----------+--------------+--------------+
| https://pypi | BASIC004  | warning  | project  | An artifact  | A package of |
| .org/pypi :: |           |          |          | has not been | type         |
| rdflib ::    |           |          |          | signed       | bdist_wheel  |
| 4.2.2        |           |          |          |              | has not been |
|              |           |          |          |              | signed       |
+--------------+-----------+----------+----------+--------------+--------------+
| https://pypi | BASIC004  | warning  | project  | An artifact  | A package of |
| .org/pypi :: |           |          |          | has not been | type sdist   |
| rdflib ::    |           |          |          | signed       | has not been |
| 4.2.2        |           |          |          |              | signed       |
+--------------+-----------+----------+----------+--------------+--------------+
| https://pypi | SPDX002   | info     | license  | SPDX License | Could not    |
| .org/pypi :: |           |          |          | not found    | map licence  |
| rdflib ::    |           |          |          |              | https://raw. |
| 4.2.2        |           |          |          |              | github.com/R |
|              |           |          |          |              | DFLib/rdflib |
|              |           |          |          |              | /master/LICE |
|              |           |          |          |              | NSE to an    |
|              |           |          |          |              | SPDX license |
+--------------+-----------+----------+----------+--------------+--------------+
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

You can run specific reports by listing them. In the command below I just ask
for the report from the `safety` reporter:

```bash
valiant report rdflib 4.2.2 safety -s
```

For multiple reports, just use a comma separator:

```bash
valiant report rdflib 4.2.2 safety,basic -s
```

You can see the list of available reports by running the `valiant config` command.

### JSON reports

You can get a copy of the report in JSON by setting the output:

```bash
valiant report rdflib 4.2.2 -o json
```

You can also produce a JSON-based findings report:

```bash
valiant report rdflib 4.2.2 -s -o json
```

As we saw in the test output examples, you can limit the reports you want:

```bash
valiant report rdflib 4.2.2 safety -s -o json
```

As a hint, it can be useful to pass the result to the handy
[`jq` tool](https://stedolan.github.io/jq/):

```bash
poetry run valiant report flask 1.1.1 -o json | jq
```

This will give you something like:

```json
[
  {
    "id": "SAFETY001",
    "coordinates": {
      "name": "rdflib",
      "version": "4.2.2",
      "repository_url": "https://pypi.org/pypi"
    },
    "level": "priority",
    "category": "security",
    "title": "Vulnerability found",
    "message": "The CLI tools in RDFLib 4.2.2 can load Python modules from the current working directory, allowing code injection, because \"python -m\" looks in this directory, as demonstrated by rdf2dot.",
    "data": {
      "name": "rdflib",
      "spec": "==4.2.2",
      "version": "4.2.2",
      "advisory": "The CLI tools in RDFLib 4.2.2 can load Python modules from the current working directory, allowing code injection, because \"python -m\" looks in this directory, as demonstrated by rdf2dot.",
      "vuln_id": "36882"
    },
    "url": "https://github.com/pyupio/safety-db"
  }
]
```

## Auditing a project

An audit is essentially a review of multiple dependencies. Valiant uses a requirements file as input. Importantly, the packages listed
in the requirements file must be pinned to a specific version. The
example below illustrates how this looks:

```
click==7.1.1
flask==1.1.1
isodate==0.6.0
itsdangerous==1.1.0
jinja2==2.11.1
markupsafe==1.1.1
numpy==1.18.2
pandas==1.0.3
pyparsing==2.4.6
python-dateutil==2.8.1
pytz==2019.3
rdflib==4.2.2
six==1.14.0
werkzeug==1.0.0
```

Thankfully, Poetry's [`export`](https://python-poetry.org/docs/cli/#export)
command makes this easy and we'll use this in the walk-through.

Let's go through the steps of creating a small project and running
an audit.

First of all, create a directory for the test project:

```bash
# Setup the project
mkdir test-valiant
cd test-valiant
```

Make sure you're running Python 3.8 (or greater). I use
[pyenv](https://github.com/pyenv/pyenv) and this makes it easy:

```bash
pyenv local 3.8.2
```

Better still, create a virtualenv - see the instructions at the
beginning of this page.

Now we set up the Poetry project and add some dependencies:

```bash
pip install poetry
poetry init -n

# Add some dependencies
poetry add flask rdflib pandas requests
```

It's now possible to export the pinned requirements file:

```bash
# Export the requirements file
poetry export --without-hashes --format requirements.txt --output requirements.txt
```

You can now run an audit of your dependencies with:

```bash
valiant audit requirements.txt
```

This will pump out a lot of information for you to sift through! It's basically
a set of reports - much like running the `valiant report` command for each package.

If you just want to view the findings across all reports:

```bash
valiant audit requirements.txt -s
```

### JSON audit reports

As with the one-off report, you can get the audit in JSON format:

```
poetry run valiant audit requirements.txt -o json
```

The findings-only listing is also available:

```
poetry run valiant audit requirements.txt -s -o json
```
