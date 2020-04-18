"""Utility cli.

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
import argparse
import pickle  # noqa: S403

from .license import SPDX_LICENSE_DATA_FILE_URL, SpdxLicenses

"""Builds a pickle file from the SPDX License json data.

This function generates the `spdx-licenses.pickle` file found in this package.

Example:
    poetry run python -m valiant.plugins.reports.spdx \
        src/valiant/plugins/reports/spdx/spdx-licenses.pickle

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
