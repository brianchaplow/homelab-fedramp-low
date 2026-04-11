"""Ingest Wazuh vulnerability state from the Wazuh Indexer into Findings.

Per ADR 0006 Deviation 5, Wazuh 4.8 removed the REST /vulnerability
endpoint. This pipeline reads every in-boundary agent's vulnerability
state from the ``wazuh-states-vulnerabilities-*`` OpenSearch index via
:class:`pipelines.common.wazuh_indexer.WazuhIndexerClient` and maps
each hit to a :class:`pipelines.common.schemas.Finding`.

Field mapping (live schema verified 2026-04-09)::

    hit['_source']['vulnerability']['id']           → cve
    hit['_source']['vulnerability']['score']['base'] → cvss_score
    hit['_source']['vulnerability']['severity']     → severity
    hit['_source']['vulnerability']['detected_at']  → discovered_date
    hit['_source']['vulnerability']['description']  → description
    hit['_source']['vulnerability']['reference']    → references (list)
    hit['_source']['package']['name']               → affected_package
    hit['_source']['agent']['name']                 → affected_host

Wazuh's own severity label is preferred over a computed one -- it
already maps CVSS v2/v3/v4 scores correctly. The CVSS-based mapping
is the fallback when ``severity`` is missing or blank. Every finding
maps to ``RA-5`` (Vulnerability Scanning) and ``SI-2`` (Flaw
Remediation) -- controls a 3PAO expects on any CVE-based POA&M item.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

from pipelines.common.logging import get_logger
from pipelines.common.schemas import Finding, Severity
from pipelines.common.wazuh_indexer import WazuhIndexerClient


logger = get_logger(__name__)


WAZUH_VULN_RELATED_CONTROLS: tuple[str, ...] = ("RA-5", "SI-2")


_SEVERITY_LABEL_MAP: dict[str, Severity] = {
    "critical": Severity.CRITICAL,
    "high": Severity.HIGH,
    "medium": Severity.MEDIUM,
    "low": Severity.LOW,
    "info": Severity.INFO,
    "informational": Severity.INFO,
    "none": Severity.INFO,
}


def severity_from_cvss(cvss_score: float | None) -> Severity:
    """Map a CVSS base score (v2/v3/v4) to a FedRAMP severity bucket.

    FedRAMP SLA windows are driven by these buckets: Critical = 15
    days, High = 30, Medium = 90, Low = 180. ``None`` falls back to
    Medium so Plan 2 never silently upgrades a blank to Low.
    """
    if cvss_score is None:
        return Severity.MEDIUM
    if cvss_score >= 9.0:
        return Severity.CRITICAL
    if cvss_score >= 7.0:
        return Severity.HIGH
    if cvss_score >= 4.0:
        return Severity.MEDIUM
    return Severity.LOW


def _severity_for(wazuh_severity: str | None, cvss_score: float | None) -> Severity:
    """Prefer Wazuh's label; fall back to cvss-based computation."""
    if wazuh_severity:
        mapped = _SEVERITY_LABEL_MAP.get(wazuh_severity.strip().lower())
        if mapped is not None:
            return mapped
    return severity_from_cvss(cvss_score)


def _parse_detected_at(value: str | None) -> datetime:
    """Parse a Wazuh indexer ``detected_at`` ISO string to a UTC datetime."""
    if not value:
        return datetime.now(timezone.utc)
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        logger.warning("unparseable detected_at '%s' -- defaulting to now()", value)
        return datetime.now(timezone.utc)


def _references_from_wazuh(raw: str | None) -> list[str]:
    """Wazuh stores ``vulnerability.reference`` as a single string, which
    may embed multiple comma-separated URLs. Split on commas and strip
    whitespace; drop empties."""
    if not raw:
        return []
    parts = [p.strip() for p in raw.split(",")]
    return [p for p in parts if p]


def wazuh_indexer_hit_to_finding(hit: dict[str, Any]) -> Finding:
    """Convert one Wazuh indexer hit to a normalized :class:`Finding`.

    Raises :class:`KeyError` on structurally broken hits (missing
    ``_source`` or ``vulnerability``) so the ingest loop can catch and
    skip them rather than crashing mid-pipeline.
    """
    source = hit["_source"]
    vuln = source["vulnerability"]
    agent = source.get("agent", {}) or {}
    package = source.get("package", {}) or {}

    cve = vuln.get("id") or "UNKNOWN-CVE"
    agent_name = agent.get("name") or "unknown-host"
    pkg_name = package.get("name") or "unknown-package"
    pkg_version = package.get("version") or ""

    score_block = vuln.get("score") or {}
    cvss_score = score_block.get("base")
    if cvss_score is not None:
        try:
            cvss_score = float(cvss_score)
        except (TypeError, ValueError):
            cvss_score = None

    description = vuln.get("description") or f"{cve} in {pkg_name}"
    description_with_pkg = f"{description} (package: {pkg_name} {pkg_version}).".strip()

    discovered = _parse_detected_at(vuln.get("detected_at"))

    return Finding(
        finding_id=f"{agent_name}:{cve}:{pkg_name}",
        title=f"{cve} in {pkg_name}",
        description=description_with_pkg,
        severity=_severity_for(vuln.get("severity"), cvss_score),
        cve=cve,
        cvss_score=cvss_score,
        affected_host=agent_name,
        affected_package=pkg_name,
        discovered_date=discovered,
        last_seen_date=datetime.now(timezone.utc),
        source_tool="wazuh-vuln",
        references=_references_from_wazuh(vuln.get("reference")),
        related_controls=list(WAZUH_VULN_RELATED_CONTROLS),
    )


def ingest_wazuh_vulns(
    indexer: WazuhIndexerClient,
    in_boundary_agent_names: Iterable[str],
) -> list[Finding]:
    """Pull vulnerabilities from the Wazuh Indexer for every named agent.

    Args:
        indexer: A :class:`WazuhIndexerClient` instance.
        in_boundary_agent_names: iterable of agent *names* (not ids) to
            include. The overlay in ``inventory/overlay.yaml`` is the
            canonical source of this list.

    Returns:
        A flat list of normalized :class:`Finding` records across all
        named agents. Malformed hits are logged and skipped.
    """
    findings: list[Finding] = []
    for agent_name in in_boundary_agent_names:
        hits = indexer.search_vulnerabilities(agent_name=agent_name)
        logger.info("agent %s: %d indexer hits", agent_name, len(hits))
        for hit in hits:
            try:
                findings.append(wazuh_indexer_hit_to_finding(hit))
            except (KeyError, TypeError) as exc:
                logger.warning(
                    "skipping malformed hit for %s: %s (hit id=%s)",
                    agent_name,
                    exc,
                    hit.get("_id", "<no id>"),
                )

    logger.info("ingested %d total in-boundary findings from Wazuh indexer", len(findings))
    return findings
