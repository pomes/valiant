"""Base classes for describing a package."""
import json

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List

from packaging.requirements import Requirement


class ArtifactMetadata(ABC):
    """Metadata for a package artifact.

    A package version usually has one or more artifacts aligned
    to it. Most releases include a source archive and a built distribution.

    See: https://packaging.python.org/specifications/distribution-formats/

    TODO: Consider the platform requirements for an artifact - e.g. macosx or
    """

    @property
    @abstractmethod
    def comment_text(self) -> str:  # pragma: no cover
        """The comment text provided in the artifact."""

    @property
    @abstractmethod
    def digests(self) -> Dict[str, str]:  # pragma: no cover
        """Provides the hashes (digests) for the artifact.

        For example, refer to
        https://pip.pypa.io/en/stable/reference/pip_install/#hash-checking-mode
        """

    @property
    @abstractmethod
    def sha256_digest(self) -> str:  # pragma: no cover
        """Convenience method to access the SHA256 hash."""

    @property
    @abstractmethod
    def signed(self) -> bool:  # pragma: no cover
        """True if the artifact was signed, False otherwise."""

    @property
    @abstractmethod
    def signature_url(self) -> str:  # pragma: no cover
        """Returns the url of the signing key for the artifact.

        Implementations should provide the URL if supported and for
        artifacts marked `has_sig=True`.

        For example, signatures can be accessed from the central PyPi
        repository by adding `.asc` to the artifact url.
        """

    @property
    @abstractmethod
    def package_type(self) -> str:  # pragma: no cover
        """The packaging type of the artifact.

        Example values:
            - sdist
            - bdist_wheel
        """

    @property
    @abstractmethod
    def python_version(self) -> str:  # pragma: no cover
        """The Python version required for the version.

        Example values:
            - source
            - py2.py3
            - py3

        See: https://www.python.org/dev/peps/pep-0425/
        See: https://www.python.org/dev/peps/pep-0508/#environment-markers
        """

    @property
    @abstractmethod
    def requires_python(self) -> List[str]:  # pragma: no cover
        """A list of Python versions supported by the artifact.

        See: Versioning spec: https://www.python.org/dev/peps/pep-0440/#version-specifiers
        """

    @property
    @abstractmethod
    def size(self) -> int:  # pragma: no cover
        """The size of the artifact in bytes."""

    @property
    @abstractmethod
    def upload_time_iso_8601(self) -> datetime:  # pragma: no cover
        """The ISO 8601-compliant timestamp of the upload.

        See: https://en.wikipedia.org/wiki/ISO_8601
        """

    @property
    @abstractmethod
    def url(self) -> str:  # pragma: no cover
        """The download URL for the artifact."""


class PackageMetadata(ABC):
    """The metadata for a Python package."""

    def _requirement_to_dict(self, req: Requirement) -> Dict:
        return {
            "name": req.name,
            "url": req.url,
            "specifiers": [
                {
                    "version": s.version,
                    "operator": s.operator,
                    "prereleases": s.prereleases,
                }
                for s in req.specifier
            ],
            "extras": [e for e in req.extras],
            "marker": f"{req.marker}" if req.marker else None,
        }

    def __str__(self) -> str:  # noqa: D105
        return self.to_json()

    def to_dict(self) -> Dict:
        """Extract a Dictionary version of the instance.

        Returns:
            That's right kids, a dictionary.
        """
        return {
            "name": self.name,
            "version": self.version,
            "summary": self.summary,
            "license": self.license,
        }

    def to_json(self) -> str:
        """Extract an instance in JSON format.

        Returns:
            JSON string rendition of the instance.
        """
        return json.dumps(self.to_dict())

    @property
    @abstractmethod
    def name(self) -> str:  # pragma: no cover
        """The name of the package."""

    @property
    @abstractmethod
    def summary(self) -> str:  # pragma: no cover
        """A brief summary of the package."""

    @property
    @abstractmethod
    def description(self) -> str:  # pragma: no cover
        """A longer description of the package."""

    @property
    @abstractmethod
    def license(self) -> str:  # pragma: no cover
        """The license assigned to the package.

        Ideally, this will match an SPDX identifier.

        See: https://spdx.org/licenses/
        See also: https://github.com/pomes/poetry/blob/master/poetry/spdx/license.py
        """

    @property
    @abstractmethod
    def version(self) -> str:  # pragma: no cover
        """The package version."""

    @property
    @abstractmethod
    def url_code(self) -> str:  # pragma: no cover
        """The website for the central codebase.

        For example: https://github.com/pomes/valiant
        """

    @property
    @abstractmethod
    def url_documentation(self) -> str:  # pragma: no cover
        """The website providing documentation for the package.

        For example: http://pomes.github.io/valiant
        """

    @property
    @abstractmethod
    def url_project(self) -> str:  # pragma: no cover
        """The project's primary website."""

    @property
    @abstractmethod
    def url_issue_tracker(self) -> str:  # pragma: no cover
        """The issue tracker for the package/project.

        For example: https://github.com/pomes/valiant/issues
        """

    @property
    @abstractmethod
    def requires_python(self) -> List[str]:  # pragma: no cover
        """Lists the Python version specifiers.

        Packaging spec:
        https://packaging.python.org/specifications/core-metadata/#requires-python

        Versioning spec: https://www.python.org/dev/peps/pep-0440/#version-specifiers

        # noqa: DAR202
        Returns:
            The list of requires-python entries
        """

    @property
    @abstractmethod
    def requires_dist(self) -> Dict[str, List[Requirement]]:  # pragma: no cover
        """A distutils-based dependency.

        See:
        https://packaging.python.org/specifications/core-metadata/#requires-dist-multiple-use

        See: PEP 508 -- Dependency specification for Python Software Packages
        https://www.python.org/dev/peps/pep-0508/


        See:
        https://setuptools.readthedocs.io/en/latest/pkg_resources.html#requirement-methods-and-attributes # noqa: B950

        Versioning spec:
            https://www.python.org/dev/peps/pep-0440/#version-specifiers

        # noqa: DAR202
        Returns:
            A dictionary of parsed Requirements with the requirement name as key
        """

    @property
    @abstractmethod
    def artifacts(self) -> List[ArtifactMetadata]:  # pragma: no cover
        """The artifacts related to the package.

        # noqa: DAR202
        Returns:
            A list of artifacts related to the package version.
        """
