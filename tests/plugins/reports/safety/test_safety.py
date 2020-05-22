"""Safety report tests.

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
    assert rpd.version == "1.9.0"


def test_safety_parameters(monkeypatch: Any) -> None:
    """Test the envvars are passed into the safety check."""
    import valiant.plugins.reports.safety.provider

    def mock_check(*args, **kwargs):  # noqa:ANN
        assert kwargs["key"] == "APIKEY"
        assert kwargs["ignore_ids"] == ["1234"]
        return []

    monkeypatch.setattr(
        valiant.plugins.reports.safety.provider, "safety_check", mock_check,
    )

    monkeypatch.setenv("SAFETY_API_KEY", "APIKEY")
    monkeypatch.setenv("SAFETY_IGNORE_IDS", "1234")

    rp = SafetyReportPlugin()
    rp.prepare_report(MockPackage(), "")


def test_safety_parameters_ignore_list(monkeypatch: Any) -> None:
    """Test the ignore list is broken up correctly."""
    import valiant.plugins.reports.safety.provider

    def mock_check(*args, **kwargs):  # noqa:ANN
        assert kwargs["key"] == "APIKEY"
        assert kwargs["ignore_ids"] == ["1234", "5678", "1357"]
        return []

    monkeypatch.setattr(
        valiant.plugins.reports.safety.provider, "safety_check", mock_check,
    )

    monkeypatch.setenv("SAFETY_API_KEY", "APIKEY")
    monkeypatch.setenv("SAFETY_IGNORE_IDS", "1234,5678,1357")

    rp = SafetyReportPlugin()
    rp.prepare_report(MockPackage(), "")


def test_safety_generate_report(monkeypatch: Any) -> None:
    """Test the generate_report method."""
    import json
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
