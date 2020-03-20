# Contributing

Apologies but I'm yet to flesh this out.

## Developing

Pre-requisites:

- [Pyenv](https://github.com/pyenv/pyenv)
- [Poetry](https://python-poetry.org/)
- [Pre-commit]()

Hint: Read the Poetry docs first as they guide you through a sound setup.

Running `pyenv local` should list out at least a 3.7 and 3.8 release - my example is:

    3.7.6
    3.8.2

Configure your local python env with:

    pyenv local 3.8.2

Once you have the codebase you can install the required packages:

    poetry install

Pre-commit is used to configure git pre-commit checks.
Please install the configuration:

    pre-commit install

You can then run the checks:

    pre-commit run --all-files

### Running tests

Look at [`noxfile.py`](noxfile.py) for the main test automation suite.

Get a list of sessions/tasks:

    nox --list

To run tests:

    nox -s tests

To lint (against Python 3.8):

    nox -rs lint-3.8


### Documentation

The site documentation uses [`mkdocs`](https://www.mkdocs.org/).
The configuration is located in [`mkdocs.yml`](mkdocs.yml).

When working on the docs it can be handy to check your work as
you go:

    mkdocs serve

To [deploy the documentation to GitHub](https://www.mkdocs.org/user-guide/deploying-your-docs/):

    mkdocs gh-deploy

This will prepare the site and push it to the `gh-pages` branch. Make sure the site's
looking good and ready to go (`mkdocs serve`) first!

### Before checking in

To check that you'll pass the pre-commit hooks, stage your files and then run:

    pre-commit run

### Useful references

| Tool | Description |
| ---- | ----------- |
| [pre-commit](https://pre-commit.com/) | Git hooks |
| [nox](https://nox.thea.codes/en/stable/index.html) | test automation |
| [pytest](https://docs.pytest.org/en/latest/) | test framework |
| [flake8](http://flake8.pycqa.org/en/latest/index.html) | linting plus plugins |
| [flake8-annotations](https://github.com/python-discord/flake8-annotations) | checks for function annotations |
| [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) | static analyzer - flags possible bugs/issues in codebase |
| [flake8-docstrings](https://gitlab.com/pycqa/flake8-docstrings) | checks docstrings - wraps [pydocstyle](https://github.com/pycqa/pydocstyle) |
| [Darglint](https://github.com/terrencepreilly/darglint) | Checks docstrings match implementation |
| [isort](https://timothycrosley.github.io/isort/) | Organises imports |
| [Black](https://black.readthedocs.io/en/stable/) | code formatter |
| [mypy](http://mypy-lang.org/) | Static type checking |
| [Bandit](https://bandit.readthedocs.io/en/latest/) | static analyzer - security issues |
| [Safety](https://pyup.io/safety/) | checks dependencies for known vulnearbilities |
| [Pytype](https://google.github.io/pytype/) | static analyzer |
| [Typeguard](https://typeguard.readthedocs.io/en/latest/) | run-time type checking |
