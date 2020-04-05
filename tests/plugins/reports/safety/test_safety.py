"""Safety report tests."""
import json
from dataclasses import dataclass
from typing import Any


from safety.safety import Vulnerability
from valiant.package import PackageCoordinates
from valiant.reports import FindingCategory, FindingLevel
from valiant.plugins.reports.safety import SafetyReportPlugin


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
    rpd = SafetyReportPlugin.report_provider_details()
    assert rpd.name == "safety"
    assert rpd.display_name == "Safety"
    assert rpd.version == "1.8.7"


def test_safety_generate_report(monkeypatch: Any) -> None:
    """Test the generate_report method."""
    import valiant.plugins.reports.safety.provider

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
        valiant.plugins.reports.safety.provider, "safety_check", mock_check,
    )

    rp = SafetyReportPlugin()
    report = rp.prepare_report(MockPackage(), "")
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

    assert f.data["name"] == "vname"
    assert f.data["spec"] == "vspec"
    assert f.data["version"] == "vversion"
    assert f.data["advisory"] == "vadvisory"
    assert f.data["vuln_id"] == "12345"

    assert f.to_dict()["level"] == FindingLevel.PRIORITY.value

    j = json.loads(f.to_json())
    assert j["level"] == FindingLevel.PRIORITY.value
