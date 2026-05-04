"""Apply Deviation Request dispositions to the OSCAL POA&M.

Reads `oscal/poam.json`, walks every poam-item, and for each item whose
title references a package covered by an active DR, mutates the
`poam-state` property to "False Positive" or "Risk Accepted" and adds a
`deviation-request` prop pointing at the DR ID. Writes the file back.

Two DRs are honored:

- FP-0002 -- packages installed but code path unreachable
  (amd64-microcode on Intel hosts, libde265-0 with no media path)
- OR-0002 -- admin-only trusted-input tooling
  (binutils suite, vim suite, patch, libelf+libdw, libxslt, busybox,
  libarchive13t64)

The renderer (pipelines/render/poam.py) skips items whose state is in
the exclusion set, so flipping state here drops the item count in the
"Open POA&M Items" sheet.

Idempotent: running twice produces no further changes -- items already
flipped to FP/RA are skipped.

Usage:
    python runbooks/apply-deviation-requests.py [--poam-json PATH]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Each DR maps to (state, package patterns). The regex is matched
# case-insensitively against the poam-item `title`. The titles look
# like "CVE-2025-1352 in Libelf1t64" -- a leading "CVE-... in <pkg>"
# pattern -- so we anchor on " in <pkg>" boundary.
DR_RULES: list[dict[str, Any]] = [
    {
        "dr_id": "FP-0002",
        "state": "False Positive",
        "rationale": "Package installed but code path unreachable on Intel-only fleet / no media path / no avahi-daemon. See deviation-requests/FP-0002-package-installed-but-unreachable.md.",
        "packages": [
            "amd64-microcode",
            "libde265-0",
            "libavahi-client3",
            "libavahi-common3",
            "libavahi-common-data",
        ],
    },
    {
        "dr_id": "OR-0002",
        "state": "Risk Accepted",
        "rationale": "Admin-only tooling with attacker-input requirement; trusted-input invocation only. See deviation-requests/OR-0002-admin-only-trusted-input-tooling.md.",
        "packages": [
            "binutils",
            "binutils-common",
            "binutils-x86-64-linux-gnu",
            "libbinutils",
            "libctf0",
            "libctf-nobfd0",
            "libgprofng0",
            "libsframe1",
            "vim",
            "vim-common",
            "vim-runtime",
            "vim-tiny",
            "xxd",
            "patch",
            "libelf1t64",
            "libdw1t64",
            "libxslt1.1",
            "busybox-static",
            "busybox-initramfs",
            "libarchive13t64",
            "tar",
            "rsync",
            "wget",
            "git",
            "git-man",
        ],
    },
]


def _build_pkg_to_dr() -> dict[str, dict[str, str]]:
    """Flatten DR_RULES into a {pkg_lower: {dr_id, state, rationale}} map."""
    out: dict[str, dict[str, str]] = {}
    for rule in DR_RULES:
        for pkg in rule["packages"]:
            out[pkg.lower()] = {
                "dr_id": rule["dr_id"],
                "state": rule["state"],
                "rationale": rule["rationale"],
            }
    return out


PKG_TO_DR = _build_pkg_to_dr()

# Match " in <package>" at the end of a title; tolerate trailing whitespace.
TITLE_PKG_RE = re.compile(r" in (\S[\S ]*?)\s*$", re.IGNORECASE)


def _extract_package(title: str) -> str | None:
    m = TITLE_PKG_RE.search(title or "")
    return m.group(1).lower() if m else None


def _set_prop(item: dict[str, Any], name: str, value: str) -> bool:
    """Insert or update a prop. Returns True if the prop was added or changed."""
    props = item.setdefault("props", [])
    for p in props:
        if p.get("name") == name:
            if p.get("value") == value:
                return False
            p["value"] = value
            return True
    props.append({"name": name, "value": value})
    return True


def apply(poam_json_path: Path) -> dict[str, int]:
    """Walk the OSCAL POA&M and flip state for items matching DR-covered packages.

    Returns a counters dict: {dr_id: items_flipped, "skipped": already_flipped, "total": all_items}.
    """
    data = json.loads(poam_json_path.read_text(encoding="utf-8"))
    items = data["plan-of-action-and-milestones"]["poam-items"]

    counters: dict[str, int] = {"total": len(items), "skipped": 0, "no_match": 0}
    for rule in DR_RULES:
        counters[rule["dr_id"]] = 0

    for item in items:
        pkg = _extract_package(item.get("title", ""))
        if not pkg:
            counters["no_match"] += 1
            continue
        rule = PKG_TO_DR.get(pkg)
        if not rule:
            counters["no_match"] += 1
            continue

        # Check if already flipped (idempotency)
        existing = {p["name"]: p.get("value") for p in item.get("props", [])}
        if existing.get("poam-state") == rule["state"] and existing.get("deviation-request") == rule["dr_id"]:
            counters["skipped"] += 1
            continue

        _set_prop(item, "poam-state", rule["state"])
        _set_prop(item, "deviation-request", rule["dr_id"])
        _set_prop(item, "deviation-rationale", rule["rationale"])
        counters[rule["dr_id"]] += 1

    poam_json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return counters


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument(
        "--poam-json",
        type=Path,
        default=Path("oscal/poam.json"),
        help="Path to OSCAL POA&M JSON (default: oscal/poam.json)",
    )
    args = ap.parse_args()

    if not args.poam_json.exists():
        print(f"ERROR: {args.poam_json} not found", file=sys.stderr)
        return 1

    counters = apply(args.poam_json)
    print(f"Total POA&M items:   {counters['total']}")
    print(f"No package match:    {counters['no_match']}")
    print(f"Already flipped:     {counters['skipped']}")
    for rule in DR_RULES:
        print(f"Flipped to {rule['state']:14s} ({rule['dr_id']}): {counters[rule['dr_id']]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
