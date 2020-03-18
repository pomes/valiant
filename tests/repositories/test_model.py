"""Ensure that the abstract models don't do anything."""

import pytest

from valiant.repositories import ArtifactMetadata, PackageMetadata


def test_artifact_metadata() -> None:
    """Ensures the ABC can't be instantiated."""
    with pytest.raises(TypeError):
        ArtifactMetadata()  # type: ignore


def test_package_metadata() -> None:
    """Ensures the ABC can't be instantiated."""
    with pytest.raises(TypeError):
        PackageMetadata()  # type: ignore
