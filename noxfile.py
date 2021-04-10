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

from typing import Callable, List, Optional

import nox

from nox.sessions import Session


package = "valiant"
nox.options.sessions = "safety", "lint", "mypy", "tests"
locations = "src", "tests", "noxfile.py"

source_location = ["src"]

supported_py_versions = ["3.8", "3.9"]
general_py_version = "3.9"


def install_with_constraints(
    session: Session,
    packages: List[str],
    include_dev: bool = True,
    callback: Optional[Callable] = None,
) -> None:
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Arguments:
        session: The Session object.
        packages: List of packages to install.
        include_dev: Export the dev dependencies from poetry.
        callback: A function to call with the session and requirements
    """
    with tempfile.NamedTemporaryFile(suffix=".txt") as requirements:
        run_args = [
            "poetry",
            "export",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
        ]

        if include_dev:
            run_args.append("--dev")

        session.run(
            *run_args, external=True,
        )

        session.install(f"--constraint={requirements.name}", *packages)

        if callback:
            callback(session, requirements.name)


@nox.session(python=general_py_version)
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
    install_with_constraints(session, packages=packages)
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

    install_with_constraints(session, packages=["black"])
    session.run("black", *args)


@nox.session(python=general_py_version)
def tidy_imports(session: Session) -> None:
    """Lint inplace using flake8-isort."""
    args = session.posargs or locations
    install_with_constraints(session, packages=["isort", "autoflake"])
    session.run(
        "autoflake",
        "--remove-all-unused-imports",
        "--in-place",
        "--recursive",
        "--ignore-init-module-imports",
        "src",
    )
    session.run("isort", "--recursive", "--apply", *args)


def install_dependencies(session: Session, requirements_file: str) -> None:
    """Installs dependencies from a requirements file."""
    session.install(f"--requirement={requirements_file}")


def safety_check(session: Session, requirements_file: str) -> None:
    """Run the safety application."""
    session.run("safety", "check", f"--file={requirements_file}", "--full-report")


@nox.session(python=general_py_version)
def safety(session: Session) -> None:
    """Scan PROD dependencies for insecure packages."""
    packages = ["safety"]
    install_with_constraints(
        session, include_dev=False, callback=safety_check, packages=packages
    )


@nox.session(python=general_py_version)
def safety_dev(session: Session) -> None:
    """Scan PROD+DEV dependencies for insecure packages."""
    packages = ["safety"]
    install_with_constraints(
        session, include_dev=True, callback=safety_check, packages=packages
    )


@nox.session(python="3.8")
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or source_location
    install_with_constraints(session, packages=["mypy", "marshmallow-dataclass"])
    session.run("mypy", *args)


@nox.session(python="3.8")
def pytype(session: Session) -> None:
    """Type-check using pytype.

    This will likely throw up errors - I'm still testing.
    """
    args = session.posargs or ["--disable=import-error", *source_location]
    install_with_constraints(session, packages=["pytype"])
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
        "./",
    ]

    install_with_constraints(
        session, packages=packages, include_dev=False, callback=install_dependencies
    )
    session.run("pytest", *args)


@nox.session(python=supported_py_versions)
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    packages = ["pytest", "pytest-mock", "pytest-datafiles", "typeguard", "./"]

    install_with_constraints(
        session, packages=packages, include_dev=False, callback=install_dependencies
    )
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session(python=supported_py_versions)
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    packages = ["xdoctest", "pygments", "./"]
    install_with_constraints(
        session, packages=packages, include_dev=False, callback=install_dependencies
    )
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python=general_py_version)
def audit(session: Session) -> None:
    """Run a Valiant audit on Valiant."""

    def generate_audit(session: Session, requirements_file: str) -> None:
        """Generate a Valiant audit."""
        from pathlib import Path

        Path("./build").mkdir(exist_ok=True)
        session.run(
            "valiant", "audit", "-o", "json", f"{requirements_file}",
        )

    packages = ["./"]
    install_with_constraints(
        session, packages=packages, include_dev=False, callback=generate_audit
    )


def generate_bom(session: Session, requirements_file: str) -> None:
    """Generate a Software Bill of Materials."""
    from pathlib import Path

    Path("./build").mkdir(exist_ok=True)
    session.run(
        "cyclonedx-py", "-j", "-i", f"{requirements_file}", "-o", "build/bom.json"
    )


@nox.session(python=general_py_version)
def bom(session: Session) -> None:
    """Generate a Software Bill of Materials."""
    packages = ["cyclonedx-bom"]
    install_with_constraints(
        session, packages=packages, include_dev=False, callback=generate_bom
    )


@nox.session(python=general_py_version)
def coverage_report(session: Session) -> None:
    """Prepare the coverage report.

    Will produce xml by default.

    json: nox -rs coverage -- json
    html: nox -rs coverage -- html
    """
    args = session.posargs or ["xml"]
    install_with_constraints(session, ["coverage[toml]"])
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
