"""Safety report tests."""
import json
from dataclasses import dataclass
from typing import Any

import valiant.reports.safety
from safety.safety import Vulnerability
from safety.util import Package as SafetyPackage
from valiant.package import PackageCoordinates
from valiant.reports import FindingCategory, FindingLevel, ReportProviderConfiguration
from valiant.reports.safety import SafetyReportProvider, VulnerabilityDictionizer


@dataclass
class MockPackage:
    """A small pkg definition."""

    name: str = "fake-lib"
    version: str = "x.y.z"
    repository_url: str = "http://repo.example.com"

    @property
    def coordinates(self) -> str:  # noqa:D102
        return PackageCoordinates(
            name=self.name, version=self.version, repository_url=self.repository_url
        )


def test_report_provider_details() -> None:
    """Basic provider check."""
    rpd = SafetyReportProvider.get_report_provider_details()
    assert rpd.name == "safety"
    assert rpd.display_name == "Safety"
    assert rpd.version == "1.8.7"


def test_report_configuration(monkeypatch: Any) -> None:
    """Check the report config."""

    def mock_check(packages, key, db_mirror, cached, ignore_ids, proxy):  # noqa:ANN
        assert packages == [SafetyPackage(key="fake-lib", version="x.y.z")]
        assert key == "mykey"
        assert db_mirror == "mydb"
        assert ignore_ids == ["id1", "id2"]
        assert not cached
        assert proxy is None
        return []

    monkeypatch.setattr(
        valiant.reports.safety, "safety_check", mock_check,
    )

    config = ReportProviderConfiguration(
        {"key": "mykey", "db": "mydb", "ignore_ids": "id1,id2"}
    )
    rp = SafetyReportProvider(ReportProviderConfiguration(config))
    rp.generate_report(MockPackage())


def test_safety_generate_report(monkeypatch: Any) -> None:
    """Test the generate_report method."""

    def mock_check(*args, **kwargs):  # noqa:ANN
        return [
            Vulnerability(
                name="vname",
                spec="vspec",
                version="vversion",
                advisory="vadvisory",
                vuln_id="12345",
            )
        ]

    monkeypatch.setattr(
        valiant.reports.safety, "safety_check", mock_check,
    )

    rp = SafetyReportProvider(ReportProviderConfiguration())
    report = rp.generate_report(MockPackage())
    assert len(report.all_findings) == 1

    f = report.all_findings[0]
    assert f.id == "SAFETY001"
    assert f.coordinates == PackageCoordinates(
        name="fake-lib", version="x.y.z", repository_url="http://repo.example.com"
    )
    assert f.title == "Vulnerability found"
    assert f.message == "vadvisory"
    assert f.level == FindingLevel.PRIORITY
    assert f.category == FindingCategory.SECURITY.value
    assert f.url == "https://github.com/pyupio/safety-db"

    assert type(f.data) == VulnerabilityDictionizer
    data = f.data.to_dict()
    assert data["name"] == "vname"
    assert data["spec"] == "vspec"
    assert data["version"] == "vversion"
    assert data["advisory"] == "vadvisory"
    assert data["vuln_id"] == "12345"

    assert f.to_dict()["level"] == FindingLevel.PRIORITY.value

    j = json.loads(f.to_json())
    assert j["level"] == FindingLevel.PRIORITY.value
