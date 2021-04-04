"""Helper assets relating to SPDX (https://spdx.org/about) licenses.

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
from dataclasses import asdict, dataclass
from dataclasses import field as dc_field
from datetime import date
from typing import Any, Dict, List, Optional, cast

import requests

from desert import desert
from marshmallow import fields
from marshmallow.exceptions import ValidationError as MarshmallowValidationError
from valiant.util import Dictionizer


"""The canonical SPDX license data in JSON format."""
SPDX_LICENSE_DATA_FILE_URL = (
    "https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json"
)


@dataclass
class SpdxLicense(Dictionizer):
    """An individual license descriptor."""

    name: str
    reference: str
    id: str = cast(str, desert.field(fields.String(data_key="licenseId")))
    is_deprecated: bool = cast(
        bool, desert.field(fields.Boolean(data_key="isDeprecatedLicenseId"))
    )
    details_url: str = cast(str, desert.field(fields.String(data_key="detailsUrl")))
    reference_number: str = cast(
        str, desert.field(fields.String(data_key="referenceNumber"))
    )
    see_also: List[str] = cast(
        List[str], desert.field(fields.List(fields.String, data_key="seeAlso"))
    )
    is_osi_approved: bool = cast(
        bool, desert.field(fields.Boolean(data_key="isOsiApproved"))
    )
    is_fsf_libre: Optional[bool] = dc_field(
        default=None, metadata=desert.metadata(fields.Boolean(data_key="isFsfLibre"))
    )

    def to_dict(self) -> Dict:  # noqa:D102
        return asdict(self)


@dataclass
class _SpdxLicenseListing:
    """Maps against the SPDX JSON format."""

    licenseListVersion: str
    licenses: List[SpdxLicense]
    releaseDate: date


class SpdxLicenses:
    """Represents a set of SPDX licenses."""

    def __init__(self, license_data: _SpdxLicenseListing):
        """New instance.

        You don't really want to call this directly.
        Instead, call one of the `loader` class methods.

        Args:
            license_data: a prepared instance of _SpdxLicenseListing
        """
        self._licenses: Dict[str, SpdxLicense] = {
            license.id: license for license in license_data.licenses
        }
        self._version = license_data.licenseListVersion
        self._release_date: date = license_data.releaseDate

    @property
    def version(self) -> str:
        """The license data version."""
        return self._version  # noqa: DAR201

    @property
    def release_date(self) -> date:
        """The release date of the data file."""
        return self._release_date  # noqa: DAR201

    def get_license(self, id: str) -> Optional[SpdxLicense]:
        """Request a specific license.

        Args:
            id: The requested license ID

        Returns:
            The associated license if available. None otherwise.
        """
        return self._licenses.get(id, None)

    @property
    def licenses(self) -> Dict[str, SpdxLicense]:
        """Returns the full set of licences."""
        return self._licenses  # noqa: DAR201

    @staticmethod
    def loader(data: Dict[str, Any]) -> "SpdxLicenses":
        """Loads the SPDX license data from a JSON string.

        Args:
            data: A dictionary structure in the expected SPDX format.

        Returns:
            An instance of SpdxLicenses if the json_s data could be loaded

        Raises:
            ValueError: If the data cannot be coreectly mapped
        """
        schema = desert.schema(_SpdxLicenseListing, meta={"partial": True})

        try:
            license_data: _SpdxLicenseListing = schema.load(data)
        except (MarshmallowValidationError, TypeError) as e:
            """
            TypeErrors seem to occur in Desert when fields such as
            `licenseId` (mapped to `id`) are missing.
            """
            raise ValueError(f"Could not parse the JSON data: {e}", e)

        return SpdxLicenses(license_data)

    @staticmethod
    def url_loader(url: str = SPDX_LICENSE_DATA_FILE_URL) -> "SpdxLicenses":
        """Loads license data from a URL.

        Args:
            url: The location of the source data.

        Returns:
            An instance of SpdxLicenses if the data could be loaded.

        Raises:
            ValueError: If the URL doesn't work or the data cannot be coreectly mapped
        """
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            raise ValueError(f"No result for {url}. Status code: {r.status_code}")

        return SpdxLicenses.loader(r.json())

    @staticmethod
    def builtin_loader() -> "SpdxLicenses":
        """Loads the license data provided by SPDX.

        A pre-built pickle file is loaded from this package. The file is
        generated by the project team using the script in `__main__.py`.

        Returns:
            The set of SPDX licences if it can be restored.

        Raises:
            ValueError: When the data cannot be loaded.
        """
        from importlib import resources as pkg_resources
        import pickle  # noqa: S403

        DATA_PACKAGE = "valiant.plugins.reports.spdx"
        DATA_FILE = "spdx-licenses.pickle"

        if not pkg_resources.is_resource(DATA_PACKAGE, DATA_FILE):  # pragma: no cover
            raise ValueError("Failed to access the data in the package.")

        with pkg_resources.open_binary(DATA_PACKAGE, DATA_FILE) as p:
            data = pickle.load(p)  # noqa: S301

        if type(data) is SpdxLicenses:
            return data

        """This is a saftey net in case the pickle file is dodgy."""
        raise ValueError(
            "The loaded datafile did not match the expected structure."
        )  # pragma: no cover
