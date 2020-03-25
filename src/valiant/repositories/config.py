"""Configuration for describing Python repositories."""
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
