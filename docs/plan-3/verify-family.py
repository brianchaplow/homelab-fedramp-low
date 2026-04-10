"""Verify a single family's assembled SSP has no empty control descriptions.

Used by the Plan 3 authoring loop as Gate 4 after every family commit.
Reads oscal/ssp.json by default (or --ssp-path for tests), filters to
the given family's implemented_requirements, and checks that every
control has at least one by-components entry with a non-empty description.

Corrected per ADR 0008 Amendment (Task 2 Gate 2 findings):
- Prose lives in by-components[].description, not statements[].description
- Un-authored controls have empty descriptions (len 0), not REPLACE_ME
- set-parameters are not present in the assembled JSON

Exit code 0 if all authored, 1 if any empty, 2 on read error.

Usage:
    .venv/Scripts/python.exe docs/plan-3/verify-family.py cm
    .venv/Scripts/python.exe docs/plan-3/verify-family.py ac --ssp-path custom.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_SSP_PATH = Path("oscal/ssp.json")


def count_empty(ssp_json: dict, family: str) -> tuple[int, int]:
    """Return (family_control_count, empty_description_count)."""
    irs = (
        ssp_json.get("system-security-plan", {})
        .get("control-implementation", {})
        .get("implemented-requirements", [])
    )
    prefix = f"{family}-"
    fam = [ir for ir in irs if ir.get("control-id", "").startswith(prefix)]
    empty = 0
    for ir in fam:
        by_components = ir.get("by-components") or []
        if not by_components:
            empty += 1
            continue
        has_prose = any(
            (bc.get("description") or "").strip()
            for bc in by_components
        )
        if not has_prose:
            empty += 1
    return len(fam), empty


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("family", help="Family code (e.g., cm, ac, au)")
    parser.add_argument(
        "--ssp-path",
        default=str(DEFAULT_SSP_PATH),
        help="Path to the assembled OSCAL SSP JSON",
    )
    args = parser.parse_args(argv)

    ssp_path = Path(args.ssp_path)
    if not ssp_path.exists():
        print(f"ERROR: SSP path does not exist: {ssp_path}", file=sys.stderr)
        return 2

    try:
        ssp_json = json.loads(ssp_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        print(f"ERROR: could not read SSP at {ssp_path}: {err}", file=sys.stderr)
        return 2

    family = args.family.lower()
    controls, empties = count_empty(ssp_json, family)
    print(f"{family}: {controls} controls, {empties} empty")
    if empties:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
