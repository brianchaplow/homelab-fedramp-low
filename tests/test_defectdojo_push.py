"""Tests for pipelines.push.defectdojo — group findings by product + import."""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from pipelines.common.schemas import Finding, Severity
from pipelines.push.defectdojo import (
    findings_to_generic_format,
    push_findings_to_defectdojo,
)


@pytest.fixture
def sample_findings() -> list[Finding]:
    return [
        Finding(
            finding_id="brisket:CVE-2024-1234:openssl",
            title="openssl heap overflow",
            description="A real CVE",
            severity=Severity.HIGH,
            cve="CVE-2024-1234",
            cvss_score=8.1,
            affected_host="brisket",
            affected_package="openssl",
            discovered_date=datetime(2026, 4, 7, tzinfo=timezone.utc),
            last_seen_date=datetime(2026, 4, 7, tzinfo=timezone.utc),
            source_tool="wazuh-vuln",
            references=["https://nvd.nist.gov/vuln/detail/CVE-2024-1234"],
            related_controls=["RA-5", "SI-2"],
        ),
        Finding(
            finding_id="haccp:CVE-2025-0001:nginx",
            title="nginx request smuggling",
            description="Another CVE",
            severity=Severity.MEDIUM,
            cve="CVE-2025-0001",
            cvss_score=5.3,
            affected_host="haccp",
            affected_package="nginx",
            discovered_date=datetime(2026, 4, 8, tzinfo=timezone.utc),
            last_seen_date=datetime(2026, 4, 8, tzinfo=timezone.utc),
            source_tool="wazuh-vuln",
            related_controls=["RA-5", "SI-2"],
        ),
    ]


# --- findings_to_generic_format -----------------------------------------


def test_findings_to_generic_format_wraps_in_findings_key(sample_findings) -> None:
    out = findings_to_generic_format(sample_findings)
    assert set(out.keys()) == {"findings"}
    assert len(out["findings"]) == 2


def test_findings_to_generic_format_carries_severity_and_host(sample_findings) -> None:
    out = findings_to_generic_format(sample_findings)
    first = out["findings"][0]
    assert first["title"] == "openssl heap overflow"
    assert first["severity"] == "High"
    # DefectDojo Generic Findings Import rejects a top-level 'host' field
    # (probed live 2026-04-09 — returned "Not allowed fields are present").
    # Hostname goes through the endpoints list instead.
    assert "host" not in first
    assert first["endpoints"] == ["brisket"]
    assert first["cve"] == "CVE-2024-1234"
    assert first["cvssv3_score"] == 8.1
    assert first["component_name"] == "openssl"
    assert first["unique_id_from_tool"] == "brisket:CVE-2024-1234:openssl"
    assert first["active"] is True
    assert first["date"] == "2026-04-07"
    assert "control:ra-5" in first["tags"]
    assert "control:si-2" in first["tags"]
    assert first["references"].startswith("https://nvd.nist.gov/")


def test_findings_to_generic_format_omits_empty_optional_fields() -> None:
    minimal = Finding(
        finding_id="x:CVE-X:pkg",
        title="x",
        description="x",
        severity=Severity.LOW,
        affected_host="x",
        discovered_date=datetime(2026, 4, 9, tzinfo=timezone.utc),
        last_seen_date=datetime(2026, 4, 9, tzinfo=timezone.utc),
        source_tool="manual",
    )
    out = findings_to_generic_format([minimal])["findings"][0]
    assert "cve" not in out
    assert "cvssv3_score" not in out
    assert "component_name" not in out
    assert "references" not in out
    assert "tags" not in out


# --- push_findings_to_defectdojo ----------------------------------------


def _mock_client(
    products: list[dict] | None = None,
    engagements: list[dict] | None = None,
) -> MagicMock:
    c = MagicMock()
    c.list_products.return_value = products or [
        {"id": 1, "name": "MSS Core - brisket"},
        {"id": 2, "name": "MSS Log Analytics - haccp"},
    ]
    c.list_engagements.return_value = engagements or []
    c.import_generic_findings.return_value = {"test_id": 999}
    c.create_engagement.side_effect = lambda product_id, name, **kw: {
        "id": 1000 + product_id,
        "name": name,
        "product": product_id,
    }
    return c


def test_push_groups_findings_by_product(sample_findings) -> None:
    client = _mock_client()
    result = push_findings_to_defectdojo(
        client=client,
        findings=sample_findings,
        host_to_product={
            "brisket": "MSS Core - brisket",
            "haccp": "MSS Log Analytics - haccp",
        },
        engagement_name="ConMon 2026-04",
    )
    assert result["imported"] == 2
    assert result["skipped"] == 0
    # One import call per product
    assert client.import_generic_findings.call_count == 2


def test_push_skips_findings_with_no_product_mapping(sample_findings) -> None:
    client = _mock_client()
    result = push_findings_to_defectdojo(
        client=client,
        findings=sample_findings,
        host_to_product={"brisket": "MSS Core - brisket"},  # haccp missing
        engagement_name="ConMon 2026-04",
    )
    assert result["imported"] == 1
    assert result["skipped"] == 1


def test_push_auto_creates_engagement_when_missing(sample_findings) -> None:
    """If the engagement doesn't exist yet, create it per-product.

    Monthly ConMon engagements should not require manual provisioning.
    """
    client = _mock_client(engagements=[])
    result = push_findings_to_defectdojo(
        client=client,
        findings=sample_findings,
        host_to_product={
            "brisket": "MSS Core - brisket",
            "haccp": "MSS Log Analytics - haccp",
        },
        engagement_name="ConMon 2026-04",
    )
    assert result["imported"] == 2
    # One create per product that has findings
    assert client.create_engagement.call_count == 2
    create_names = {
        call.kwargs.get("name") or call.args[1] if len(call.args) > 1 else call.kwargs["name"]
        for call in client.create_engagement.call_args_list
    }
    assert create_names == {"ConMon 2026-04"}


def test_push_uses_existing_engagement_when_present(sample_findings) -> None:
    client = _mock_client(
        engagements=[
            {"id": 77, "name": "ConMon 2026-04", "product": 1},
            {"id": 88, "name": "ConMon 2026-04", "product": 2},
        ]
    )
    result = push_findings_to_defectdojo(
        client=client,
        findings=sample_findings,
        host_to_product={
            "brisket": "MSS Core - brisket",
            "haccp": "MSS Log Analytics - haccp",
        },
        engagement_name="ConMon 2026-04",
    )
    assert result["imported"] == 2
    # No engagement creation — both already existed
    client.create_engagement.assert_not_called()


def test_push_raises_on_unknown_product(sample_findings) -> None:
    client = _mock_client(
        products=[{"id": 1, "name": "MSS Core - brisket"}]
    )
    with pytest.raises(ValueError, match="MSS Log Analytics"):
        push_findings_to_defectdojo(
            client=client,
            findings=sample_findings,
            host_to_product={
                "brisket": "MSS Core - brisket",
                "haccp": "MSS Log Analytics - haccp",  # not in products
            },
            engagement_name="ConMon 2026-04",
        )
