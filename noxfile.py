"""Nox sessions.

Based on https://github.com/cjolowicz/hypermodern-python/blob/master/noxfile.py
Please refer to src/valiant/third-party/hypermodern-python/LICENSE for original
copyright and license details.

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
import tempfile

from typing import Any

import nox

from nox.sessions import Session


package = "valiant"
nox.options.sessions = "safety", "lint", "mypy", "tests"
locations = "src", "tests", "noxfile.py"

supported_py_versions = ["3.8", "3.9"]
general_py_version = "3.9"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Arguments:
        session: The Session object.
        args: Command-line arguments for pip.
        kwargs: Additional keyword arguments for Session.install.
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        # print(requirements.read())
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=supported_py_versions)
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    packages = [
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-copyright",
        "darglint",
    ]
    install_with_constraints(session, *packages)
    session.run("flake8", *args)


@nox.session(python=general_py_version)
def tidy(session: Session) -> None:
    """Run all tidy up actions."""
    tidy_imports(session)
    black(session)


@nox.session(python=general_py_version)
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=general_py_version)
def tidy_imports(session: Session) -> None:
    """Lint inplace using flake8-isort."""
    args = session.posargs or locations
    install_with_constraints(session, "isort", "autoflake")
    session.run(
        "autoflake",
        "--remove-all-unused-imports",
        "--in-place",
        "--recursive",
        "--ignore-init-module-imports",
        "src",
    )
    session.run("isort", "--recursive", "--apply", *args)


@nox.session(python=general_py_version)
def safety(session: Session) -> None:
    """Scan PROD dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=general_py_version)
def safety_dev(session: Session) -> None:
    """Scan PROD+DEV dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile(delete=False) as requirements:
        session.run(
            "poetry",
            "export",
            "--format=requirements.txt",
            "--dev",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=supported_py_versions)
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    install_with_constraints(session, *["mypy", "marshmallow-dataclass"])
    session.run("mypy", *args)


@nox.session(python=supported_py_versions)
def pytype(session: Session) -> None:
    """Type-check using pytype.

    This likely won't work until PyType supports Python >= 3.7
      - Roadmap on https://google.github.io/pytype/
      - https://github.com/google/pytype/issues/440
    """
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints(session, "pytype")
    session.run("pytype", *args)


@nox.session(python=supported_py_versions)
def tests(session: Session) -> None:
    """Run the test suite.

    Get coverage by adding --cov:
        nox -rs tests -- --cov
    """
    args = session.posargs or []
    packages = [
        "coverage[toml]",
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "pytest-datafiles",
        "cleo",
    ]

    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session, *packages,
    )
    session.run("pytest", *args)


@nox.session(python=supported_py_versions)
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    packages = ["pytest", "pytest-mock", "pytest-datafiles", "typeguard"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, *packages)
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session(python=supported_py_versions)
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    packages = ["xdoctest"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, *packages)
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python=general_py_version)
def coverage_report(session: Session) -> None:
    """Prepare the coverage report.

    Will produce xml by default.

    json: nox -rs coverage -- json
    html: nox -rs coverage -- html
    """
    args = session.posargs or ["xml"]
    install_with_constraints(session, "coverage[toml]")
    session.run("coverage", *args, "--fail-under=90")


@nox.session(python=general_py_version)
def docs(session: Session) -> None:
    """Build the documentation with mkdocs."""
    session.install("mkdocs~=1.1")
    session.run("mkdocs", "build", "--clean")


@nox.session(python=general_py_version)
def docs_serve(session: Session) -> None:
    """Start server to view docs."""
    session.install("mkdocs~=1.1")
    session.run("mkdocs", "serve")


@nox.session(python=general_py_version)
def docs_publish(session: Session) -> None:
    """Publish the documentation with mkdocs."""
    session.install("mkdocs~=1.1")
    session.run("mkdocs", "gh-deploy", "--clean")
