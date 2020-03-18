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

from .. import ArtifactMetadata, PackageMetadata, ValidationError


@dataclass
class Downloads:
    """The (unused?) download counts for a package."""

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
    description_content_type: str
    docs_url: Optional[str]
    download_url: str
    downloads: Downloads
    home_page: str
    keywords: str
    license: str
    maintainer: str
    maintainer_email: str
    name: str
    package_url: str
    platform: str
    project_url: str
    project_urls: Dict[str, str]
    release_url: str
    requires_dist: List[str]
    requires_python: str
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
    requires_python: str
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

    def __init__(self, package_data: Dict):
        """Constructor.

        Args:
            package_data: A dictionary based on the JSON structure returned by the PyPi API.
                          See: https://warehouse.readthedocs.io/api-reference/json/

        Raises:
            ValidationError: when the data could not be correctly mapped.
        """
        try:
            self._pkg = desert.schema(PyPiPackage).load(package_data)
        except marshmallow.exceptions.ValidationError as ve:
            raise ValidationError(f"Could not validate the JSON data: {ve}") from ve

        self._requires_dist: Dict[str, List[Requirement]] = {}
        for item in self._pkg.info.requires_dist:
            req = Requirement(item)
            if req.name not in self._requires_dist:
                self._requires_dist[req.name] = [req]
            else:
                self._requires_dist[req.name].append(req)

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
        # TODO: Consider use of the classifier if needed
        return self._pkg.info.license

    @property
    def version(self) -> str:  # noqa: D102
        return self._pkg.info.version

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

        # noqa: DAR202
        Returns:
            A dictionary of parsed Requirements with the requirement name as key
        """
        # TODO: Fill this in - it'll need to map the URLs
