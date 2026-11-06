"""Consistency checks on committed (tracked) OSCAL artifacts and SSP sources.

These guard the package-completeness claims in the README and CLAUDE.md:

- every committed OSCAL artifact parses under the Trestle OSCAL models
- the assembled SSP implements exactly the FedRAMP Rev 5 Low baseline
  (156 controls), with no duplicates and nothing outside the baseline
- the Trestle markdown workspace and the ssp/controls mirror each hold one
  file per Low control
- oscal/ssp.json matches the Trestle-assembled SSP

They read only files in the repository; nothing touches a network.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LOW_CATALOG = (
    REPO_ROOT / "trestle-workspace" / "catalogs" / "fedramp-rev5-low-resolved" / "catalog.json"
)
SSP_PATHS = [
    REPO_ROOT / "oscal" / "ssp.json",
    REPO_ROOT / "trestle-workspace" / "system-security-plans" / "mss-ssp"
    / "system-security-plan.json",
]
EXPECTED_LOW_COUNT = 156


def _walk_controls(node: dict, out: list[str]) -> None:
    for group in node.get("groups", []):
        _walk_controls(group, out)
    for control in node.get("controls", []):
        out.append(control["id"])
        _walk_controls(control, out)


@pytest.fixture(scope="module")
def low_baseline() -> set[str]:
    ids: list[str] = []
    _walk_controls(json.loads(LOW_CATALOG.read_text(encoding="utf-8"))["catalog"], ids)
    return set(ids)


def _committed_oscal_files() -> list[Path]:
    files = [
        REPO_ROOT / "oscal" / "ssp.json",
        REPO_ROOT / "oscal" / "component-definition.json",
    ]
    files += sorted((REPO_ROOT / "conmon-submissions").glob("*/oscal/*.json"))
    return [f for f in files if f.exists()]


def test_low_baseline_has_expected_size(low_baseline: set[str]) -> None:
    assert len(low_baseline) == EXPECTED_LOW_COUNT


@pytest.mark.parametrize(
    "path", _committed_oscal_files(), ids=lambda p: str(p.relative_to(REPO_ROOT))
)
def test_committed_oscal_artifact_parses(path: Path) -> None:
    from trestle.oscal.component import ComponentDefinition
    from trestle.oscal.poam import PlanOfActionAndMilestones
    from trestle.oscal.ssp import SystemSecurityPlan

    models = {
        "system-security-plan": SystemSecurityPlan,
        "plan-of-action-and-milestones": PlanOfActionAndMilestones,
        "component-definition": ComponentDefinition,
    }
    doc = json.loads(path.read_text(encoding="utf-8"))
    (root_key,) = doc.keys()
    assert root_key in models, f"unexpected OSCAL root {root_key!r}"
    models[root_key].parse_obj(doc[root_key])


@pytest.mark.parametrize("path", SSP_PATHS, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_ssp_implements_exactly_the_low_baseline(path: Path, low_baseline: set[str]) -> None:
    ssp = json.loads(path.read_text(encoding="utf-8"))["system-security-plan"]
    ids = [r["control-id"] for r in ssp["control-implementation"]["implemented-requirements"]]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    assert duplicates == []
    assert sorted(low_baseline - set(ids)) == [], "Low controls missing from SSP"
    assert sorted(set(ids) - low_baseline) == [], "SSP controls outside the Low baseline"


@pytest.mark.parametrize("subdir", ["trestle-workspace/mss-ssp", "ssp/controls"])
def test_markdown_sources_cover_the_low_baseline(subdir: str, low_baseline: set[str]) -> None:
    stems = {p.stem for p in (REPO_ROOT / subdir).glob("*/*.md")}
    assert sorted(low_baseline - stems) == []
    assert sorted(stems - low_baseline) == []


def test_oscal_ssp_matches_trestle_assembled_ssp() -> None:
    a, b = (json.loads(p.read_text(encoding="utf-8")) for p in SSP_PATHS)
    assert a == b, "oscal/ssp.json is stale; re-run ./pipelines.sh ssp-assemble and copy"
