"""Configuration for describing Python repositories.

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
from typing import Dict, Optional
from urllib.parse import ParseResult, urlparse, urlunparse

from valiant.util import Dictionizer


@dataclass(frozen=True)
class RepositoryConfiguration(Dictionizer):
    """A Python package repository.

    Working from https://pip.pypa.io/en/stable/user_guide/#basic-authentication-credentials

    Attributes:
        name: A human-friendly name
        base_url: The repository URL such as https://pypi.org/pypi
                  Don't include things like `/simple` in the base_url.
        username: A username for the password
        password: The access password (accompanies a username)
        token: An access token (used instead of username:password)
        repository_type: The software used to host the repository
    """

    name: str
    base_url: str
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    repository_type: str = "unknown"

    def to_dict(self) -> Dict:  # noqa:D102
        return asdict(self)

    def get_access_url(self) -> str:
        """Provides the full url with credentials.

        Returns:
            The access url for the repository
        """
        url_segments: ParseResult = urlparse(self.base_url)

        if self.token:
            netloc = f"{self.token}@{url_segments.netloc}"
        elif self.username:
            netloc = f"{self.username}:{self.password}@{url_segments.netloc}"
        else:
            netloc = url_segments.netloc

        url = ParseResult(
            scheme=url_segments.scheme,
            netloc=netloc,
            path=url_segments.path,
            params=url_segments.params,
            query=url_segments.query,
            fragment=url_segments.fragment,
        )
        return urlunparse(url)
