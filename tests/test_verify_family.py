"""Unit test for docs/plan-3/verify-family.py.

verify-family.py is the Gate 4 helper that the Plan 3 authoring loop
runs after every family commit. It reads oscal/ssp.json, filters to a
single family's implemented_requirements, checks that every control has
non-empty by-components[].description, and exits non-zero if any are
empty (indicating an un-authored control).

Corrected per ADR 0008 Amendment (Task 2 Gate 2 findings):
- Prose lives in by-components[].description, not statements[].description
- Un-authored controls have empty descriptions, not REPLACE_ME
- set-parameters are not present in the assembled JSON, so not checked
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "docs" / "plan-3" / "verify-family.py"
VENV_PYTHON = REPO_ROOT / ".venv" / "Scripts" / "python.exe"


def _write_ssp(tmp_path: Path, irs: list[dict]) -> Path:
    """Write a minimal SSP JSON with the given implemented_requirements."""
    ssp = {
        "system-security-plan": {
            "uuid": "00000000-0000-0000-0000-000000000000",
            "metadata": {
                "title": "Test SSP",
                "last-modified": "2026-04-09T00:00:00-00:00",
                "version": "0.0.0",
                "oscal-version": "1.1.2",
            },
            "import-profile": {"href": "trestle://profiles/fedramp-rev5-low/profile.json"},
            "system-characteristics": {
                "system-ids": [{"id": "test"}],
                "system-name": "test",
                "description": "test",
                "security-sensitivity-level": "low",
                "system-information": {
                    "information-types": [
                        {
                            "uuid": "00000000-0000-0000-0000-000000000001",
                            "title": "t",
                            "description": "t",
                            "confidentiality-impact": {"base": "fips-199-low"},
                            "integrity-impact": {"base": "fips-199-low"},
                            "availability-impact": {"base": "fips-199-low"},
                        }
                    ]
                },
                "security-impact-level": {
                    "security-objective-confidentiality": "fips-199-low",
                    "security-objective-integrity": "fips-199-low",
                    "security-objective-availability": "fips-199-low",
                },
                "status": {"state": "other"},
                "authorization-boundary": {"description": "t"},
            },
            "system-implementation": {
                "users": [{"uuid": "00000000-0000-0000-0000-000000000002", "title": "t"}],
                "components": [
                    {
                        "uuid": "00000000-0000-0000-0000-000000000003",
                        "type": "this-system",
                        "title": "t",
                        "description": "t",
                        "status": {"state": "operational"},
                    }
                ],
            },
            "control-implementation": {
                "description": "t",
                "implemented-requirements": irs,
            },
        }
    }
    path = tmp_path / "ssp.json"
    path.write_text(json.dumps(ssp), encoding="utf-8")
    return path


def _run(ssp_path: Path, family: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(VENV_PYTHON), str(SCRIPT), family, "--ssp-path", str(ssp_path)],
        capture_output=True,
        text=True,
    )


def test_family_with_authored_prose_exits_zero(tmp_path):
    """A control with non-empty by-components description is authored."""
    irs = [
        {
            "uuid": "00000000-0000-0000-0000-000000000010",
            "control-id": "cm-2",
            "by-components": [
                {
                    "component-uuid": "00000000-0000-0000-0000-000000000003",
                    "uuid": "00000000-0000-0000-0000-000000000011",
                    "description": "Baseline configuration is git-tracked.",
                }
            ],
        }
    ]
    ssp_path = _write_ssp(tmp_path, irs)
    result = _run(ssp_path, "cm")
    assert result.returncode == 0, result.stderr
    assert "cm: 1 controls, 0 empty" in result.stdout


def test_family_with_empty_description_exits_nonzero(tmp_path):
    """A control with empty by-components description is un-authored."""
    irs = [
        {
            "uuid": "00000000-0000-0000-0000-000000000010",
            "control-id": "cm-2",
            "by-components": [
                {
                    "component-uuid": "00000000-0000-0000-0000-000000000003",
                    "uuid": "00000000-0000-0000-0000-000000000011",
                    "description": "",
                }
            ],
        }
    ]
    ssp_path = _write_ssp(tmp_path, irs)
    result = _run(ssp_path, "cm")
    assert result.returncode != 0
    assert "1 empty" in result.stdout


def test_family_with_no_by_components_exits_nonzero(tmp_path):
    """A control with no by-components at all is un-authored."""
    irs = [
        {
            "uuid": "00000000-0000-0000-0000-000000000010",
            "control-id": "cm-2",
        }
    ]
    ssp_path = _write_ssp(tmp_path, irs)
    result = _run(ssp_path, "cm")
    assert result.returncode != 0
    assert "1 empty" in result.stdout


def test_family_filter_ignores_other_families(tmp_path):
    """AC control with empty desc should not affect cm family check."""
    irs = [
        {
            "uuid": "00000000-0000-0000-0000-000000000010",
            "control-id": "ac-1",
            "by-components": [
                {
                    "component-uuid": "00000000-0000-0000-0000-000000000003",
                    "uuid": "00000000-0000-0000-0000-000000000012",
                    "description": "",
                }
            ],
        },
        {
            "uuid": "00000000-0000-0000-0000-000000000013",
            "control-id": "cm-2",
            "by-components": [
                {
                    "component-uuid": "00000000-0000-0000-0000-000000000003",
                    "uuid": "00000000-0000-0000-0000-000000000014",
                    "description": "Real prose here.",
                }
            ],
        },
    ]
    ssp_path = _write_ssp(tmp_path, irs)
    result = _run(ssp_path, "cm")
    assert result.returncode == 0, result.stderr
    assert "cm: 1 controls, 0 empty" in result.stdout


def test_empty_family_exits_zero(tmp_path):
    """A family with no controls in the SSP is treated as clean."""
    ssp_path = _write_ssp(tmp_path, [])
    result = _run(ssp_path, "cm")
    assert result.returncode == 0
    assert "cm: 0 controls, 0 empty" in result.stdout


def test_mixed_authored_and_unauthored_reports_count(tmp_path):
    """Family with 2 authored + 1 empty should report 1 empty."""
    irs = [
        {
            "uuid": "00000000-0000-0000-0000-000000000010",
            "control-id": "cm-1",
            "by-components": [{"component-uuid": "c", "uuid": "u1", "description": "Authored."}],
        },
        {
            "uuid": "00000000-0000-0000-0000-000000000011",
            "control-id": "cm-2",
            "by-components": [{"component-uuid": "c", "uuid": "u2", "description": "Authored."}],
        },
        {
            "uuid": "00000000-0000-0000-0000-000000000012",
            "control-id": "cm-4",
            "by-components": [{"component-uuid": "c", "uuid": "u3", "description": ""}],
        },
    ]
    ssp_path = _write_ssp(tmp_path, irs)
    result = _run(ssp_path, "cm")
    assert result.returncode != 0
    assert "cm: 3 controls, 1 empty" in result.stdout
