"""Base classes for describing a package."""
from abc import abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List

from packaging.requirements import Requirement
from valiant.util import Dictionizer

from .classifier import Classifier


class ArtifactMetadata(Dictionizer):
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
        """True if the artifact was signed, False otherwise.

        For further info, check out the --sign option in twine.

        See: https://github.com/pypa/twine#why-should-i-use-this
        """

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

    def to_dict(self) -> Dict:  # noqa:DAR102
        return {
            "comment_text": self.comment_text,
            "digests": self.digests,
            "sha256_digest": self.sha256_digest,
            "signed": self.signed,
            "signature_url": self.signature_url,
            "package_type": self.package_type,
            "python_version": self.python_version,
            "requires_python": self.requires_python,
            "size": self.size,
            "upload_time_iso_8601": self.upload_time_iso_8601.isoformat(),
            "url": self.url,
        }


class ArtifactMetadataImpl(ArtifactMetadata):
    """Basic implementation of ArtifactMetadata."""

    def __init__(
        self,
        comment_text: str,
        digests: Dict[str, str],
        sha256_digest: str,
        signed: bool,
        signature_url: str,
        package_type: str,
        python_version: str,
        requires_python: List[str],
        size: int,
        upload_time_iso_8601: datetime,
        url: str,
    ):  # noqa: D107
        self._comment_text = comment_text
        self._digests = digests
        self._sha256_digest = sha256_digest
        self._signed = signed
        self._signature_url = signature_url
        self._package_type = package_type
        self._python_version = python_version
        self._requires_python = requires_python
        self._size = size
        self._upload_time_iso_8601 = upload_time_iso_8601
        self._url = url

    @property
    def comment_text(self) -> str:  # pragma: no cover
        """The comment text provided in the artifact."""
        return self._comment_text  # noqa:DAR201

    @property
    def digests(self) -> Dict[str, str]:  # pragma: no cover
        """Provides the hashes (digests) for the artifact."""
        return self._digests  # noqa:DAR201

    @property
    def sha256_digest(self) -> str:  # pragma: no cover
        """Convenience method to access the SHA256 hash."""
        return self._sha256_digest  # noqa:DAR201

    @property
    def signed(self) -> bool:  # pragma: no cover
        """True if the artifact was signed, False otherwise."""
        return self._signed  # noqa:DAR201

    @property
    def signature_url(self) -> str:  # pragma: no cover
        """Returns the url of the signing key for the artifact."""
        return self._signature_url  # noqa:DAR201

    @property
    def package_type(self) -> str:  # pragma: no cover
        """The packaging type of the artifact."""
        return self._package_type  # noqa:DAR201

    @property
    def python_version(self) -> str:  # pragma: no cover
        """The Python version required for the version."""
        return self._python_version  # noqa:DAR201

    @property
    def requires_python(self) -> List[str]:  # pragma: no cover
        """A list of Python versions supported by the artifact."""
        return self._requires_python  # noqa:DAR201

    @property
    def size(self) -> int:  # pragma: no cover
        """The size of the artifact in bytes."""
        return self._size  # noqa:DAR201

    @property
    def upload_time_iso_8601(self) -> datetime:  # pragma: no cover
        """The ISO 8601-compliant timestamp of the upload."""
        return self._upload_time_iso_8601  # noqa:DAR201

    @property
    def url(self) -> str:  # pragma: no cover
        """The download URL for the artifact."""
        return self._url  # noqa:DAR201


@dataclass
class PackageCoordinates(Dictionizer):
    """An approach to locating a package based on repo, name and version.

    This is based on the Maven approach. It might be useful.

    See: http://maven.apache.org/pom.html
    """

    name: str
    version: str
    repository_url: str

    def to_dict(self) -> Dict:  # noqa: D102
        return asdict(self)

    def __str__(self) -> str:
        """String representation.

        Returns:
            A coordinator described using the classifier format.
        """
        return f"{self.repository_url} :: {self.name} :: {self.version}"


class PackageMetadata(Dictionizer):
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
            "classifiers": self.classifiers,
            "url_project": self.url_project,
            "url_code": self.url_code,
            "url_issue_tracker": self.url_issue_tracker,
            "url_documentation": self.url_documentation,
            "artifacts": [a.to_dict() for a in self.artifacts],
        }

    @property
    def coordinates(self) -> PackageCoordinates:
        """The package coordinates for this metadata."""
        return PackageCoordinates(  # noqa:DAR201
            name=self.name, version=self.version, repository_url=self.repository_url
        )

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
    def repository_url(self) -> str:  # pragma: no cover
        """The URL from whence this package info came."""

    @property
    @abstractmethod
    def license(self) -> str:  # pragma: no cover
        """The license assigned to the package.

        Ideally, this will match an SPDX identifier.

        See: https://packaging.python.org/specifications/core-metadata/#license
        See: https://spdx.org/licenses/
        """

    @property
    @abstractmethod
    def version(self) -> str:  # pragma: no cover
        """The package version."""

    @property
    @abstractmethod
    def classifiers(self) -> List[str]:  # pragma: no cover
        """The classifiers listed against the package.

        You can use the Classifier class in this package to parse
        classifiers if needed.
        """

    @property
    @abstractmethod
    def classifiers_parsed(self) -> List[Classifier]:  # pragma: no cover
        """The parsed classifiers listed against the package."""

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
