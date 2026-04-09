"""Tests for pipelines.ingest.wazuh_vulns — Wazuh indexer → Finding records.

Per ADR 0006 Deviation 5, this pipeline reads vulnerability state from
the Wazuh Indexer (OpenSearch) index ``wazuh-states-vulnerabilities-*``
via :class:`pipelines.common.wazuh_indexer.WazuhIndexerClient`, NOT
from the removed Wazuh REST /vulnerability endpoint.
"""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from pipelines.common.schemas import Finding, FindingState, Severity
from pipelines.ingest.wazuh_vulns import (
    WAZUH_VULN_RELATED_CONTROLS,
    ingest_wazuh_vulns,
    severity_from_cvss,
    wazuh_indexer_hit_to_finding,
)


def _hit(
    agent_name: str = "brisket",
    agent_id: str = "015",
    cve: str = "CVE-2025-1234",
    severity: str = "High",
    base: float | None = 7.5,
    pkg_name: str = "openssl",
    pkg_version: str = "3.0.13",
    detected_at: str = "2026-04-09T16:53:18.428Z",
    description: str = "heap overflow",
    reference: str | None = "https://nvd.nist.gov/vuln/detail/CVE-2025-1234",
) -> dict:
    vuln: dict = {
        "id": cve,
        "severity": severity,
        "description": description,
        "detected_at": detected_at,
    }
    if base is not None:
        vuln["score"] = {"base": base, "version": "3.1"}
    if reference is not None:
        vuln["reference"] = reference
    return {
        "_index": "wazuh-states-vulnerabilities-wazuh.manager",
        "_id": f"{agent_id}_{cve}_{pkg_name}",
        "_source": {
            "agent": {"id": agent_id, "name": agent_name},
            "package": {"name": pkg_name, "version": pkg_version, "type": "deb"},
            "vulnerability": vuln,
        },
    }


# --- severity_from_cvss ---------------------------------------------------


def test_severity_from_cvss_maps_to_fedramp_buckets() -> None:
    assert severity_from_cvss(9.5) == Severity.CRITICAL
    assert severity_from_cvss(9.0) == Severity.CRITICAL
    assert severity_from_cvss(7.0) == Severity.HIGH
    assert severity_from_cvss(8.9) == Severity.HIGH
    assert severity_from_cvss(4.0) == Severity.MEDIUM
    assert severity_from_cvss(6.9) == Severity.MEDIUM
    assert severity_from_cvss(1.0) == Severity.LOW
    assert severity_from_cvss(3.9) == Severity.LOW
    assert severity_from_cvss(None) == Severity.MEDIUM


# --- wazuh_indexer_hit_to_finding ----------------------------------------


def test_hit_to_finding_basic_shape() -> None:
    f = wazuh_indexer_hit_to_finding(_hit())
    assert isinstance(f, Finding)
    assert f.finding_id == "brisket:CVE-2025-1234:openssl"
    assert f.cve == "CVE-2025-1234"
    assert f.cvss_score == 7.5
    assert f.severity == Severity.HIGH
    assert f.affected_host == "brisket"
    assert f.affected_package == "openssl"
    assert f.source_tool == "wazuh-vuln"
    assert f.state == FindingState.OPEN
    assert list(WAZUH_VULN_RELATED_CONTROLS) == f.related_controls


def test_hit_to_finding_prefers_wazuh_severity_over_cvss() -> None:
    """Wazuh already maps CVSS v2/v3/v4 to a severity label consistently;
    use its label as the primary source and only fall back to cvss_score
    if Wazuh's severity is missing or blank."""
    # Wazuh says Critical but base score is only 5.0 — we trust Wazuh
    hit = _hit(severity="Critical", base=5.0, cve="CVE-X")
    f = wazuh_indexer_hit_to_finding(hit)
    assert f.severity == Severity.CRITICAL


def test_hit_to_finding_falls_back_to_cvss_when_severity_missing() -> None:
    hit = _hit(severity="", base=8.1, cve="CVE-Y")
    f = wazuh_indexer_hit_to_finding(hit)
    assert f.severity == Severity.HIGH


def test_hit_to_finding_handles_missing_score_block() -> None:
    hit = _hit(severity="Low", base=None, cve="CVE-Z")
    f = wazuh_indexer_hit_to_finding(hit)
    assert f.cvss_score is None
    assert f.severity == Severity.LOW


def test_hit_to_finding_parses_iso_datetime() -> None:
    hit = _hit(detected_at="2026-04-09T16:53:18.428Z")
    f = wazuh_indexer_hit_to_finding(hit)
    assert f.discovered_date.tzinfo is not None
    assert f.discovered_date.year == 2026
    assert f.discovered_date.month == 4
    assert f.discovered_date.day == 9


def test_hit_to_finding_wraps_reference_string_in_list() -> None:
    """Wazuh's indexer emits .vulnerability.reference as a single string
    (may contain multiple comma-separated URLs). Finding.references is a
    list, so the string must be wrapped (split on comma+space if needed)."""
    hit = _hit(
        reference="https://ubuntu.com/security/CVE-2025-1234, https://www.cve.org/CVERecord?id=CVE-2025-1234"
    )
    f = wazuh_indexer_hit_to_finding(hit)
    assert len(f.references) == 2
    assert f.references[0].startswith("https://ubuntu.com/")
    assert f.references[1].startswith("https://www.cve.org/")


def test_hit_to_finding_handles_missing_reference() -> None:
    hit = _hit(reference=None)
    f = wazuh_indexer_hit_to_finding(hit)
    assert f.references == []


def test_hit_to_finding_description_includes_package_version() -> None:
    hit = _hit(description="heap overflow", pkg_name="openssl", pkg_version="3.0.13")
    f = wazuh_indexer_hit_to_finding(hit)
    assert "openssl" in f.description
    assert "3.0.13" in f.description


def test_hit_to_finding_related_controls_are_ra5_and_si2() -> None:
    f = wazuh_indexer_hit_to_finding(_hit())
    assert f.related_controls == ["RA-5", "SI-2"]


# --- ingest_wazuh_vulns ---------------------------------------------------


def test_ingest_wazuh_vulns_calls_indexer_for_each_agent() -> None:
    """One call to WazuhIndexerClient.search_vulnerabilities per agent
    name, and the results are concatenated into a single flat list."""
    indexer = MagicMock()
    indexer.search_vulnerabilities.side_effect = lambda agent_name, **_: [
        _hit(agent_name=agent_name, cve=f"CVE-{agent_name}-1"),
        _hit(agent_name=agent_name, cve=f"CVE-{agent_name}-2", pkg_name="nginx"),
    ]

    findings = ingest_wazuh_vulns(indexer, ["brisket", "haccp"])

    assert len(findings) == 4
    hosts = {f.affected_host for f in findings}
    assert hosts == {"brisket", "haccp"}
    cves = {f.cve for f in findings}
    assert cves == {
        "CVE-brisket-1",
        "CVE-brisket-2",
        "CVE-haccp-1",
        "CVE-haccp-2",
    }
    # Two calls, one per agent
    assert indexer.search_vulnerabilities.call_count == 2


def test_ingest_wazuh_vulns_empty_agent_list_returns_empty() -> None:
    indexer = MagicMock()
    assert ingest_wazuh_vulns(indexer, []) == []
    indexer.search_vulnerabilities.assert_not_called()


def test_ingest_wazuh_vulns_skips_malformed_hit() -> None:
    """A hit with a missing _source.vulnerability should not crash the
    whole pipeline — the bad hit is logged and skipped."""
    indexer = MagicMock()
    indexer.search_vulnerabilities.return_value = [
        _hit(cve="CVE-GOOD"),
        {"_source": {"agent": {"name": "brisket"}}},  # missing vulnerability
    ]
    findings = ingest_wazuh_vulns(indexer, ["brisket"])
    assert len(findings) == 1
    assert findings[0].cve == "CVE-GOOD"
