"""Tests for pipelines.build.oscal_poam -- DefectDojo findings → OSCAL POA&M."""
from __future__ import annotations

import json
import re
from datetime import date, timedelta
from pathlib import Path

import pytest

from pipelines.build.oscal_poam import (
    SLA_DAYS,
    build_poam_from_defectdojo,
    sla_due_date,
)


UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)


# --- FedRAMP Low ConMon SLA windows --------------------------------------


def test_sla_days_match_fedramp_low_windows() -> None:
    """FedRAMP Low ConMon Strategy Guide -- Critical 15, High 30,
    Moderate 90, Low 180. Not the plan text's 30/90/180/365 which
    were a pre-execution mistake documented in ADR 0006 amendment."""
    assert SLA_DAYS == {
        "Critical": 15,
        "High": 30,
        "Medium": 90,
        "Low": 180,
    }


def test_sla_due_date_applies_correct_window() -> None:
    base = date(2026, 4, 7)
    assert sla_due_date(base, "Critical") == base + timedelta(days=15)
    assert sla_due_date(base, "High") == base + timedelta(days=30)
    assert sla_due_date(base, "Medium") == base + timedelta(days=90)
    assert sla_due_date(base, "Low") == base + timedelta(days=180)


def test_sla_due_date_unknown_severity_falls_back_to_low() -> None:
    base = date(2026, 4, 7)
    assert sla_due_date(base, "Info") == base + timedelta(days=180)
    assert sla_due_date(base, "") == base + timedelta(days=180)


# --- POA&M builder -------------------------------------------------------


def _sample_finding(**overrides) -> dict:
    base = {
        "id": 1,
        "title": "openssl heap overflow",
        "severity": "High",
        "cve": "CVE-2024-1234",
        "active": True,
        "is_mitigated": False,
        "false_p": False,
        "risk_accepted": False,
        "date": "2026-04-07",
        "host": "brisket",
        "description": "test desc",
        "tags": ["control:ra-5", "control:si-2"],
    }
    base.update(overrides)
    return base


def test_build_poam_writes_file(tmp_path: Path) -> None:
    out = tmp_path / "poam.json"
    path = build_poam_from_defectdojo([_sample_finding()], out)
    assert path == out
    assert out.exists()


def test_build_poam_top_level_shape(tmp_path: Path) -> None:
    out = tmp_path / "poam.json"
    build_poam_from_defectdojo([_sample_finding()], out)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "plan-of-action-and-milestones" in data
    poam = data["plan-of-action-and-milestones"]
    assert UUID_RE.match(poam["uuid"])
    assert "metadata" in poam
    assert poam["metadata"]["title"]
    assert poam["metadata"]["oscal-version"] == "1.1.2"
    assert "system-id" in poam
    assert "poam-items" in poam


def test_build_poam_item_properties(tmp_path: Path) -> None:
    out = tmp_path / "poam.json"
    build_poam_from_defectdojo([_sample_finding()], out)
    item = json.loads(out.read_text(encoding="utf-8"))[
        "plan-of-action-and-milestones"
    ]["poam-items"][0]
    assert UUID_RE.match(item["uuid"])
    assert item["title"] == "openssl heap overflow"
    assert item["description"] == "test desc"
    props = {p["name"]: p["value"] for p in item["props"]}
    assert props["severity"] == "High"
    assert props["cve"] == "CVE-2024-1234"
    assert props["discovered-date"] == "2026-04-07"
    assert props["scheduled-completion"] == "2026-05-07"  # High = +30 days
    assert props["poam-state"] == "Open"
    assert props["affected-host"] == "brisket"
    assert props["related-controls"] == "RA-5, SI-2"


def test_build_poam_empty_props_are_omitted(tmp_path: Path) -> None:
    """OSCAL rejects empty prop values -- same rule as Task 8."""
    finding = _sample_finding(cve=None, description="")
    out = tmp_path / "poam.json"
    build_poam_from_defectdojo([finding], out)
    item = json.loads(out.read_text(encoding="utf-8"))[
        "plan-of-action-and-milestones"
    ]["poam-items"][0]
    prop_names = {p["name"] for p in item["props"]}
    assert "cve" not in prop_names
    for p in item["props"]:
        assert p["value"]


def test_build_poam_state_mapping(tmp_path: Path) -> None:
    cases = [
        (_sample_finding(false_p=True), "False Positive"),
        (_sample_finding(risk_accepted=True, active=False), "Deviated"),
        (_sample_finding(is_mitigated=True, active=False), "Completed"),
        (_sample_finding(active=False, is_mitigated=False), "Closed"),
        (_sample_finding(active=True), "Open"),
    ]
    for finding, expected_state in cases:
        out = tmp_path / f"poam-{expected_state}.json"
        build_poam_from_defectdojo([finding], out)
        item = json.loads(out.read_text(encoding="utf-8"))[
            "plan-of-action-and-milestones"
        ]["poam-items"][0]
        props = {p["name"]: p["value"] for p in item["props"]}
        assert props["poam-state"] == expected_state, f"state mismatch for {expected_state}"


def test_build_poam_critical_gets_15_day_window(tmp_path: Path) -> None:
    finding = _sample_finding(severity="Critical", date="2026-04-01")
    out = tmp_path / "poam.json"
    build_poam_from_defectdojo([finding], out)
    item = json.loads(out.read_text(encoding="utf-8"))[
        "plan-of-action-and-milestones"
    ]["poam-items"][0]
    props = {p["name"]: p["value"] for p in item["props"]}
    assert props["scheduled-completion"] == "2026-04-16"  # April 1 + 15 days


def test_build_poam_last_modified_is_iso_with_tz(tmp_path: Path) -> None:
    out = tmp_path / "poam.json"
    build_poam_from_defectdojo([_sample_finding()], out)
    stamp = json.loads(out.read_text(encoding="utf-8"))[
        "plan-of-action-and-milestones"
    ]["metadata"]["last-modified"]
    assert stamp.endswith("Z") or re.search(r"[+-]\d{2}:\d{2}$", stamp)
