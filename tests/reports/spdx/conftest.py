"""Test configuration.

See: https://docs.pytest.org/en/latest/pythonpath.html
"""
import pytest


# See:
# https://docs.pytest.org/en/latest/monkeypatch.html#global-patch-example-preventing-requests-from-remote-operations # noqa: B950
@pytest.fixture(autouse=True)
def no_requests(monkeypatch) -> None:  # noqa: ANN001
    """Prevent requests lib from performing real requests.

    Remove requests.sessions.Session.request for all tests.
    """
    monkeypatch.delattr("requests.sessions.Session.request")
