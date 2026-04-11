"""Tests for pipelines.common.schemas -- normalized Finding and InventoryComponent."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from pipelines.common.schemas import (
    Finding,
    FindingState,
    InventoryComponent,
    Severity,
)


def _dt(y: int = 2026, m: int = 4, d: int = 9) -> datetime:
    return datetime(y, m, d, tzinfo=timezone.utc)


def test_finding_minimal_defaults_state_open_and_controls_empty() -> None:
    f = Finding(
        finding_id="brisket:CVE-2024-1234:nginx",
        title="nginx CVE-2024-1234",
        description="A theoretical vuln",
        severity=Severity.HIGH,
        affected_host="brisket",
        discovered_date=_dt(),
        last_seen_date=_dt(),
        source_tool="wazuh-vuln",
    )
    assert f.state == FindingState.OPEN
    assert f.severity == Severity.HIGH
    assert f.related_controls == []
    assert f.references == []


def test_finding_with_cve_and_controls() -> None:
    f = Finding(
        finding_id="brisket:CVE-2024-1234:nginx",
        title="nginx CVE-2024-1234",
        description="A theoretical vuln",
        severity=Severity.CRITICAL,
        cve="CVE-2024-1234",
        cvss_score=9.8,
        affected_host="brisket",
        affected_package="nginx",
        discovered_date=_dt(),
        last_seen_date=_dt(),
        source_tool="wazuh-vuln",
        references=["https://nvd.nist.gov/vuln/detail/CVE-2024-1234"],
        related_controls=["RA-5", "SI-2"],
    )
    assert f.cve == "CVE-2024-1234"
    assert f.cvss_score == 9.8
    assert f.related_controls == ["RA-5", "SI-2"]


def test_finding_rejects_unknown_severity() -> None:
    with pytest.raises(ValueError):
        Finding(
            finding_id="x",
            title="x",
            description="x",
            severity="ExtraSpicy",  # type: ignore[arg-type]
            affected_host="x",
            discovered_date=_dt(),
            last_seen_date=_dt(),
            source_tool="wazuh-vuln",
        )


def test_finding_rejects_unknown_source_tool() -> None:
    with pytest.raises(ValueError):
        Finding(
            finding_id="x",
            title="x",
            description="x",
            severity=Severity.LOW,
            affected_host="x",
            discovered_date=_dt(),
            last_seen_date=_dt(),
            source_tool="nessus",  # type: ignore[arg-type]
        )


def test_finding_is_frozen() -> None:
    f = Finding(
        finding_id="x",
        title="x",
        description="x",
        severity=Severity.LOW,
        affected_host="x",
        discovered_date=_dt(),
        last_seen_date=_dt(),
        source_tool="manual",
    )
    with pytest.raises((TypeError, ValueError)):
        f.title = "tampered"  # type: ignore[misc]


def test_inventory_component_defaults() -> None:
    c = InventoryComponent(
        unique_id="MSS-HOST-001",
        hostname="brisket",
        ip_address="10.10.20.30",
        is_virtual=False,
        asset_type="Server",
        function="SIEM Manager",
    )
    assert c.boundary == "in"
    assert c.location == "On-prem homelab rack, Virginia"
    assert c.authenticated_scan is True
    assert c.in_latest_scan is True
    assert c.is_public is False


def test_inventory_component_rejects_unknown_asset_type() -> None:
    with pytest.raises(ValueError):
        InventoryComponent(
            unique_id="x",
            hostname="x",
            ip_address="x",
            is_virtual=False,
            asset_type="Toaster",  # type: ignore[arg-type]
            function="x",
        )


def test_inventory_component_rejects_unknown_boundary() -> None:
    with pytest.raises(ValueError):
        InventoryComponent(
            unique_id="x",
            hostname="x",
            ip_address="x",
            is_virtual=False,
            asset_type="VM",
            function="x",
            boundary="maybe",  # type: ignore[arg-type]
        )


def test_inventory_component_is_frozen() -> None:
    c = InventoryComponent(
        unique_id="x",
        hostname="x",
        ip_address="x",
        is_virtual=False,
        asset_type="VM",
        function="x",
    )
    with pytest.raises((TypeError, ValueError)):
        c.hostname = "tampered"  # type: ignore[misc]
