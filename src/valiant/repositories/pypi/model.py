"""Data model for the PyPi JSON API.

The data classes defined here aim to map closely to the JSON
returned by the PyPi API.

See: https://warehouse.readthedocs.io/api-reference/json/

TODO: Consider "yanked" artifacts: https://www.python.org/dev/peps/pep-0592/
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from desert import desert, marshmallow
from packaging.requirements import Requirement
from valiant.package import (
    ArtifactMetadata,
    ArtifactMetadataImpl,
    Classifier,
    PackageMetadata,
)

from .. import ValidationError


@dataclass
class Downloads:
    """The (unused?) download counts for a package.

    See https://packaging.python.org/guides/analyzing-pypi-package-downloads/
    """

    last_day: int
    last_month: int
    last_week: int


@dataclass
class Info:
    """The package metadata.

    See also: https://packaging.python.org/specifications/core-metadata/
    """

    author: str
    author_email: str
    bugtrack_url: Optional[str]
    classifiers: List[str]
    description: str
    description_content_type: Optional[str]
    docs_url: Optional[str]
    download_url: str
    downloads: Downloads
    home_page: str
    keywords: Optional[str]
    license: str
    maintainer: Optional[str]
    maintainer_email: Optional[str]
    name: str
    package_url: str
    platform: str
    project_url: str
    project_urls: Dict[str, str]
    release_url: str
    requires_dist: Optional[List[str]]
    requires_python: Optional[str]
    summary: str
    version: str


@dataclass
class Release:
    """A single release artifact for a package.

    PyPi seems to return a list of all releases regardless
    of if you designate a version.
    """

    comment_text: str
    digests: Dict[str, str]
    downloads: int
    filename: str
    has_sig: bool
    md5_digest: str
    packagetype: str
    python_version: str
    requires_python: Optional[str]
    size: int
    upload_time: datetime
    upload_time_iso_8601: datetime
    url: str


@dataclass
class ArtifactUrl:
    """An artifact (i.e. file) for a package."""

    comment_text: str
    digests: Dict[str, str]
    downloads: int
    filename: str
    has_sig: bool
    md5_digest: str
    packagetype: str
    python_version: str
    requires_python: Optional[str]
    size: int
    upload_time: datetime
    upload_time_iso_8601: datetime
    url: str


@dataclass
class PyPiPackage:
    """Represents the package metadata returned from pypi.org."""

    info: Info
    last_serial: int
    releases: Dict[str, List[Release]]
    urls: List[ArtifactUrl]


@dataclass
class PyPiPackageMetadata(PackageMetadata):
    """Provides the required PackageMetadata interface for a PyPiPackage."""

    def __init__(self, repository_url: str, package_data: Dict):
        """Constructor.

        Args:
            repository_url: The URL for the repo that provided this metadata.
            package_data: A dictionary based on the JSON structure returned by the PyPi API.
                          See: https://warehouse.readthedocs.io/api-reference/json/

        Raises:
            ValidationError: when the data could not be correctly mapped.
        """
        self._repository_url = repository_url
        self._parsed_classifiers: Optional[List[Classifier]] = None
        self._artifacts: List[ArtifactMetadata] = []

        try:
            self._pkg = desert.schema(PyPiPackage).load(package_data)
        except marshmallow.exceptions.ValidationError as ve:
            raise ValidationError(f"Could not validate the JSON data: {ve}") from ve

        self._requires_dist: Dict[str, List[Requirement]] = {}
        if self._pkg.info.requires_dist:
            for item in self._pkg.info.requires_dist:
                req = Requirement(item)
                if req.name not in self._requires_dist:
                    self._requires_dist[req.name] = [req]
                else:
                    self._requires_dist[req.name].append(req)

        # Process the urls into artifacts
        for entry in self._pkg.urls:
            self._artifacts.append(
                ArtifactMetadataImpl(
                    comment_text=entry.comment_text,
                    digests=entry.digests,
                    sha256_digest=entry.digests.get("sha256", None),
                    signed=entry.has_sig,
                    signature_url=f"{entry.url}.asc",
                    package_type=entry.packagetype,
                    python_version=entry.python_version,
                    requires_python=entry.requires_python,
                    size=entry.size,
                    upload_time_iso_8601=entry.upload_time_iso_8601,
                    url=entry.url,
                )
            )

    @property
    def name(self) -> str:  # noqa: D102
        return self._pkg.info.name

    @property
    def description(self) -> str:  # noqa: D102
        return self._pkg.info.description

    @property
    def summary(self) -> str:  # noqa: D102
        return self._pkg.info.summary

    @property
    def license(self) -> str:  # noqa: D102
        return self._pkg.info.license

    @property
    def classifiers(self) -> List[str]:  # noqa: D102
        """The classifiers listed against the package.

        Returns:
            A list of classifier strings.
        """
        return self._pkg.info.classifiers

    @property
    def classifiers_parsed(self) -> List[Classifier]:  # noqa: D102
        """The parsed classifiers listed against the package.

        Returns:
            A list of parsed classifiers.
        """
        if not self._parsed_classifiers:
            self._parsed_classifiers = []
            for item in self.classifiers:
                self._parsed_classifiers.append(Classifier.parse(item))

        return self._parsed_classifiers

    @property
    def version(self) -> str:  # noqa: D102
        return self._pkg.info.version

    @property
    def repository_url(self) -> str:  # noqa: D102
        return self._repository_url

    @property
    def url_code(self) -> str:  # noqa: D102
        return self._pkg.info.project_urls.get("Code", "")

    @property
    def url_documentation(self) -> str:  # noqa: D102
        if self._pkg.info.docs_url:
            return self._pkg.info.docs_url

        return self._pkg.info.project_urls.get("Documentation", "")

    @property
    def url_project(self) -> str:  # noqa: D102
        if self._pkg.info.home_page:
            return self._pkg.info.home_page

        if self._pkg.info.project_url:
            return self._pkg.info.project_url

        return self._pkg.info.project_urls.get("Homepage", "")

    @property
    def url_issue_tracker(self) -> str:  # noqa: D102
        if self._pkg.info.bugtrack_url:
            return self._pkg.info.bugtrack_url

        return self._pkg.info.project_urls.get("Issue tracker", "")

    @property
    def requires_dist(self) -> Dict[str, List[Requirement]]:
        """A distutils-based dependency.

        See:
        https://packaging.python.org/specifications/core-metadata/#requires-dist-multiple-use

        See: PEP 508 -- Dependency specification for Python Software Packages
        https://www.python.org/dev/peps/pep-0508/

        See:
        https://setuptools.readthedocs.io/en/latest/pkg_resources.html#requirement-methods-and-attributes # noqa: B950

        Versioning spec:
            https://www.python.org/dev/peps/pep-0440/#version-specifiers

        Returns:
            A dictionary of parsed Requirements with the requirement name as key
            See: (https://packaging.pypa.io/en/latest/requirements/)
        """
        return self._requires_dist

    @property
    def requires_python(self) -> List[str]:
        """Lists the Python version specifiers.

        Packaging spec:
        https://packaging.python.org/specifications/core-metadata/#requires-python

        Versioning spec:
        https://www.python.org/dev/peps/pep-0440/#version-specifiers

        Returns:
            The list of requires-python entries
        """
        return [p.strip() for p in self._pkg.info.requires_python.split(",")]

    @property
    def artifacts(self) -> List[ArtifactMetadata]:
        """A distutils-based dependency.

        See:
        https://packaging.python.org/specifications/core-metadata/#requires-dist-multiple-use

        See: PEP 508 -- Dependency specification for Python Software Packages
        https://www.python.org/dev/peps/pep-0508/


        See:
        https://setuptools.readthedocs.io/en/latest/pkg_resources.html#requirement-methods-and-attributes # noqa: B950

        Versioning spec:
            https://www.python.org/dev/peps/pep-0440/#version-specifiers


        Returns:
            A dictionary of parsed Requirements with the requirement name as key
        """
        return self._artifacts
