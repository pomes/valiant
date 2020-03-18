"""Nox sessions.

Based on https://github.com/cjolowicz/hypermodern-python/blob/master/noxfile.py

Docs available at https://nox.thea.codes/en/stable/
"""
import tempfile

from typing import Any

import nox

from nox.sessions import Session


package = "valiant"
nox.options.sessions = "lint", "safety", "mypy", "tests"
locations = "src", "tests", "noxfile.py"

supported_py_versions = ["3.8"]
general_py_version = "3.8"


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
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=supported_py_versions)
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-isort",
        "darglint",
    )
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
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=general_py_version)
def safety_dev(session: Session) -> None:
    """Scan PROD+DEV dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--format=requirements.txt",
            "--without-hashes",
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
    install_with_constraints(session, "mypy")
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
    """Run the test suite."""
    args = session.posargs or ["--cov"]
    packages = [
        "coverage[toml]",
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "pytest-datafiles",
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
def coverage(session: Session) -> None:
    """Prepare the coverage report.

    Will produce xml by default.

    json: nox -rs coverage -- json
    html: nox -rs coverage -- html
    """
    args = session.posargs or ["xml"]
    install_with_constraints(session, "coverage[toml]")
    session.run("coverage", *args, "--fail-under=0")


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
