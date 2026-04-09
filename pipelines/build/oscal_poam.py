"""Build an OSCAL Plan of Action and Milestones (POA&M) from DefectDojo findings.

Each DefectDojo finding becomes one OSCAL POA&M item with the FedRAMP
ConMon SLA-based scheduled completion date. The input shape is
DefectDojo's REST API finding dict (the ``/api/v2/findings/`` result
shape), not the normalized Finding schema — this is intentional so
that a future Task 12.5 can backfill POA&M items from Nessus or
tenable.io without re-implementing the whole builder.

**FedRAMP Low ConMon SLA windows** (per the FedRAMP Continuous
Monitoring Strategy Guide, applied per severity):

================  ====  ==============================
Severity          Days  Notes
================  ====  ==============================
Critical          15    Immediate remediation
High              30
Moderate/Medium   90
Low               180
================  ====  ==============================

Plan 2's draft text specified 30/90/180/365 as the SLA windows. Those
values are wrong — FedRAMP Low uses 15/30/90/180. Corrected here and
documented as an ADR 0006 amendment (Task 12).

The POA&M output conforms to NIST OSCAL 1.1.2. The same empty-prop
rule from Task 8 applies: prop values must not be empty strings, so
optional fields are only emitted when populated.
"""
from __future__ import annotations

import json
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from pipelines.common.logging import get_logger


logger = get_logger(__name__)


OSCAL_VERSION: str = "1.1.2"


# FedRAMP Low ConMon SLA windows, keyed by severity label. Any severity
# not in this dict falls back to the Low window (180 days).
SLA_DAYS: dict[str, int] = {
    "Critical": 15,
    "High": 30,
    "Medium": 90,
    "Low": 180,
}


def sla_due_date(discovered: date, severity: str) -> date:
    """Return the FedRAMP Low ConMon SLA due date for a finding.

    Unknown severities (including ``Info`` and ``""``) fall back to the
    Low window (180 days) — the longest, not the shortest, so the
    caller can adjust upward if they discover the severity mid-cycle.
    """
    days = SLA_DAYS.get(severity, SLA_DAYS["Low"])
    return discovered + timedelta(days=days)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _finding_state(finding: dict[str, Any]) -> str:
    """Map DefectDojo state flags to a POA&M state string.

    Evaluation order matters: false-positive > risk-accepted > mitigated
    > active > closed. A finding that is both ``false_p=True`` and
    ``is_mitigated=True`` is reported as False Positive, not Completed.
    """
    if finding.get("false_p"):
        return "False Positive"
    if finding.get("risk_accepted"):
        return "Deviated"
    if finding.get("is_mitigated"):
        return "Completed"
    if finding.get("active"):
        return "Open"
    return "Closed"


def _controls_from_tags(tags: list[str]) -> list[str]:
    """Extract NIST 800-53 control ids from DefectDojo ``control:*`` tags."""
    controls = []
    for tag in tags or []:
        if tag.startswith("control:"):
            controls.append(tag.split(":", 1)[1].upper())
    return controls


def _finding_to_poam_item(finding: dict[str, Any]) -> dict[str, Any]:
    """Convert one DefectDojo finding dict to an OSCAL POA&M item dict."""
    discovered_str = finding.get("date") or date.today().isoformat()
    discovered = date.fromisoformat(discovered_str)
    severity = finding.get("severity", "Medium")
    due = sla_due_date(discovered, severity)
    state = _finding_state(finding)
    controls = _controls_from_tags(finding.get("tags", []))

    props: list[dict[str, str]] = []

    def _maybe(name: str, value: str | None) -> None:
        if value:
            props.append({"name": name, "value": value})

    _maybe("weakness-id", str(finding.get("id") or ""))
    _maybe("severity", severity)
    _maybe("cve", finding.get("cve") or None)
    _maybe("discovered-date", discovered.isoformat())
    _maybe("scheduled-completion", due.isoformat())
    _maybe("poam-state", state)
    _maybe("affected-host", finding.get("host") or None)
    if controls:
        _maybe("related-controls", ", ".join(controls))

    return {
        "uuid": str(uuid.uuid4()),
        "title": finding.get("title") or "Untitled finding",
        "description": finding.get("description") or finding.get("title") or "No description",
        "props": props,
    }


def build_poam_from_defectdojo(
    findings: list[dict[str, Any]],
    output_path: Path,
    title: str = "Managed SOC Service POA&M",
    version: str = "0.1.0",
    system_id: str = "managed-soc-service",
) -> Path:
    """Build and write an OSCAL POA&M JSON from a list of DefectDojo findings.

    Args:
        findings: list of DefectDojo finding dicts (the ``results`` of
            ``/api/v2/findings/``).
        output_path: where to write the POA&M JSON. Parent directories
            are created if missing.
        title: POA&M metadata title.
        version: POA&M metadata version string.
        system_id: the system-id value the POA&M is attached to.

    Returns:
        The ``output_path`` that was written.
    """
    poam_items = [_finding_to_poam_item(f) for f in findings]

    poam: dict[str, Any] = {
        "plan-of-action-and-milestones": {
            "uuid": str(uuid.uuid4()),
            "metadata": {
                "title": title,
                "last-modified": _now_iso(),
                "version": version,
                "oscal-version": OSCAL_VERSION,
            },
            "system-id": {
                "id": system_id,
                "identifier-type": "https://ietf.org/rfc/rfc4122",
            },
            "poam-items": poam_items,
        }
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(poam, indent=2), encoding="utf-8")
    logger.info(
        "wrote OSCAL POA&M with %d items to %s", len(poam_items), output_path
    )
    return output_path
