"""Tests for ArtifactMetadataImpl."""
import json

from datetime import datetime

import pytest

from valiant.package import ArtifactMetadata, ArtifactMetadataImpl


@pytest.fixture
def basic_artifact() -> ArtifactMetadata:
    """Based on Flask 1.1.1."""
    return ArtifactMetadataImpl(  # noqa:DAR201
        comment_text="No comment",
        digests={
            "md5": "b5cc35905a936f5f64e51421d1ebe29c",
            "sha256": "45eb5a6fd193d6cf7e0cf5d8a5b31f83d5faae0293695626f539a823e93b13f6",
        },
        sha256_digest="45eb5a6fd193d6cf7e0cf5d8a5b31f83d5faae0293695626f539a823e93b13f6",
        signed=True,
        signature_url="https://files.pythonhosted.org/packages/9b/93/628509b8d5dc749656a9641f4caf13540e2cdec85276964ff8f43bbb1d3b/Flask-1.1.1-py2.py3-none-any.whl.asc",  # noqa:B950
        package_type="bdist_wheel",
        python_version="py2.py3",
        requires_python=[
            ">=2.7",
            "!=3.0.*",
            "!=3.1.*",
            "!=3.2.*",
            "!=3.3.*",
            "!=3.4.*",
        ],
        size=94457,
        upload_time_iso_8601=datetime(2019, 7, 8, 18, 0, 28, 597456),
        url="https://files.pythonhosted.org/packages/9b/93/628509b8d5dc749656a9641f4caf13540e2cdec85276964ff8f43bbb1d3b/Flask-1.1.1-py2.py3-none-any.whl",  # noqa:B950
    )


def test_basic_artifact_dict(basic_artifact: ArtifactMetadata) -> None:
    """Validate to_dict."""
    d = basic_artifact.to_dict()
    assert d["comment_text"] == "No comment"


def test_basic_artifact_json(basic_artifact: ArtifactMetadata) -> None:
    """Validate to_json."""
    d = json.loads(basic_artifact.to_json())
    assert d["comment_text"] == "No comment"
