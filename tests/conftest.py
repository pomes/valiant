"""Test configuration.

See: https://docs.pytest.org/en/latest/pythonpath.html
"""
import pytest


# See:
# https://docs.pytest.org/en/latest/monkeypatch.html#global-patch-example-preventing-requests-from-remote-operations # noqa: B950
@pytest.fixture(autouse=True)
def no_requests(monkeypatch):  # noqa: ANN001, ANN201
    """Prevent requests lib from performing real requests.

    Remove requests.sessions.Session.request for all tests.
    """
    # I just can't seem to get the tests to run with the line below.
    # Any thoughts would be really appreciated

    # monkeypatch.delattr("requests.sessions.Session.request")

    monkeypatch.setattr("requests_cache.install_cache", lambda *a, **kw: None)
