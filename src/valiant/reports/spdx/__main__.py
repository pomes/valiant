"""Utility cli."""
import argparse
import pickle  # noqa: S403

from . import SPDX_LICENSE_DATA_FILE_URL, SpdxLicenses


"""Builds a pickle file from the SPDX License json data.

This function generates the `spdx-licenses.pickle` file found in this package.

Example:
    python -m valiant.reports.spdx valiant/reports/spdx/spdx-licenses.pickle

Returns:
    The path of the pickle file
"""


parser = argparse.ArgumentParser(
    description="Pickle the SPDX license data.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--url",
    type=str,
    default=SPDX_LICENSE_DATA_FILE_URL,
    help="The url for the SPDX License JSON file",
)

parser.add_argument("output_file", type=str, help="The file path for the pickle file")

args = parser.parse_args()

licenses: SpdxLicenses = SpdxLicenses.url_loader(args.url)
with open(args.output_file, "wb") as f:
    pickle.dump(licenses, f)
