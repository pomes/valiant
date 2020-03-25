"""Tests the PackageCoordinates class."""
from valiant.package import PackageCoordinates


def test_coord_basic() -> None:
    """Basic coordinate tests."""
    pc = PackageCoordinates(
        name="flask", version="1.1.1", repository_url="https://pypi.org"
    )
    assert str(pc) == "https://pypi.org :: flask :: 1.1.1"

    d = pc.to_dict()
    assert d["name"] == "flask"
    assert d["version"] == "1.1.1"
    assert d["repository_url"] == "https://pypi.org"
