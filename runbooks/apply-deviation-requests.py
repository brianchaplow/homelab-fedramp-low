"""Apply approved Deviation Request dispositions to an OSCAL POA&M.

The rule table below is derived from the approved deviation-request documents.
Application is deliberately fail-closed: every candidate item is preflighted for
DR lifecycle, documented host scope, and documented CVE scope before any item is
changed or the POA&M file is written.

Usage:
    python runbooks/apply-deviation-requests.py [--poam-json PATH] [--as-of YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Sequence


APPROVED_STATUS = "Approved"
TITLE_PKG_RE = re.compile(r" in (\S[\S ]*?)\s*$", re.IGNORECASE)
TITLE_CVE_RE = re.compile(r"\bCVE-\d{4}-\d{4,}\b", re.IGNORECASE)


@dataclass(frozen=True)
class DeviationScope:
    """Package-specific scope documented by a deviation request."""

    package: str
    hosts: frozenset[str]
    cves: frozenset[str] | None = None


@dataclass(frozen=True)
class DeviationRule:
    """Lifecycle, disposition, and package scopes for one deviation request."""

    dr_id: str
    status: str
    effective_on: date
    expires_on: date
    state: str
    rationale: str
    document: str
    scopes: tuple[DeviationScope, ...]


@dataclass(frozen=True)
class PlannedMutation:
    """One mutation approved by preflight."""

    item_index: int
    rule: DeviationRule


@dataclass(frozen=True)
class PreflightViolation:
    """A reason the POA&M cannot be safely mutated."""

    item_index: int
    item_id: str
    dr_id: str
    reason: str

    def render(self) -> str:
        return f"item[{self.item_index}] {self.item_id} ({self.dr_id}): {self.reason}"


class PreflightError(ValueError):
    """Raised when one or more candidate items fail DR preflight."""

    def __init__(self, violations: Sequence[PreflightViolation]) -> None:
        self.violations = tuple(violations)
        super().__init__(f"{len(self.violations)} deviation preflight violation(s)")


@dataclass(frozen=True)
class PreflightResult:
    """A complete, non-mutating application plan."""

    mutations: tuple[PlannedMutation, ...]
    counters: dict[str, int]


def _scope(
    package: str,
    hosts: Sequence[str],
    cves: Sequence[str] | None = None,
) -> DeviationScope:
    return DeviationScope(
        package=package.casefold(),
        hosts=frozenset(host.casefold() for host in hosts),
        cves=frozenset(cve.upper() for cve in cves) if cves is not None else None,
    )


FOUR_HOSTS = ("brisket", "haccp", "dojo", "regscale")
FP_0003_CVES = (
    "CVE-2019-12067",
    "CVE-2020-13791",
    "CVE-2020-24352",
    "CVE-2020-25741",
    "CVE-2020-25742",
    "CVE-2020-25743",
    "CVE-2020-35503",
    "CVE-2021-20255",
    "CVE-2021-3735",
    "CVE-2022-3872",
    "CVE-2023-1386",
    "CVE-2024-8612",
)


# The status and effective date come from each document's Reviewer approval
# section. Package, host, and optional CVE scopes come from its linked-items table.
DR_RULES: tuple[DeviationRule, ...] = (
    DeviationRule(
        dr_id="FP-0002",
        status=APPROVED_STATUS,
        effective_on=date(2026, 5, 4),
        expires_on=date(2027, 5, 4),
        state="False Positive",
        rationale=(
            "Package installed but code path unreachable on the documented hosts. "
            "See deviation-requests/FP-0002-package-installed-but-unreachable.md."
        ),
        document="deviation-requests/FP-0002-package-installed-but-unreachable.md",
        scopes=(
            _scope("amd64-microcode", FOUR_HOSTS),
            _scope("libde265-0", ("brisket", "haccp")),
            _scope("libavahi-client3", ("brisket",)),
            _scope("libavahi-common3", ("brisket",)),
            _scope("libavahi-common-data", ("brisket",)),
        ),
    ),
    DeviationRule(
        dr_id="FP-0003",
        status=APPROVED_STATUS,
        effective_on=date(2026, 5, 4),
        expires_on=date(2026, 8, 4),
        state="False Positive",
        rationale=(
            "The documented QEMU CVEs affect hypervisor device-emulation code, not "
            "qemu-guest-agent. See deviation-requests/"
            "FP-0003-qemu-guest-agent-hypervisor-cves.md."
        ),
        document="deviation-requests/FP-0003-qemu-guest-agent-hypervisor-cves.md",
        scopes=(
            _scope("qemu-guest-agent", ("dojo", "regscale"), FP_0003_CVES),
        ),
    ),
    DeviationRule(
        dr_id="OR-0002",
        status=APPROVED_STATUS,
        effective_on=date(2026, 5, 4),
        expires_on=date(2026, 8, 4),
        state="Risk Accepted",
        rationale=(
            "Admin-only tooling with an attacker-input requirement on the documented "
            "hosts. See deviation-requests/OR-0002-admin-only-trusted-input-tooling.md."
        ),
        document="deviation-requests/OR-0002-admin-only-trusted-input-tooling.md",
        scopes=(
            _scope("binutils", ("brisket", "haccp")),
            _scope("binutils-common", ("brisket", "haccp")),
            _scope("binutils-x86-64-linux-gnu", ("brisket", "haccp")),
            _scope("libbinutils", ("brisket", "haccp")),
            _scope("libctf0", ("brisket", "haccp")),
            _scope("libctf-nobfd0", ("brisket", "haccp")),
            _scope("libgprofng0", ("brisket", "haccp")),
            _scope("libsframe1", ("brisket", "haccp")),
            _scope("vim", FOUR_HOSTS),
            _scope("vim-common", FOUR_HOSTS),
            _scope("vim-runtime", FOUR_HOSTS),
            _scope("vim-tiny", FOUR_HOSTS),
            _scope("xxd", FOUR_HOSTS),
            _scope("patch", FOUR_HOSTS),
            _scope("libelf1t64", FOUR_HOSTS),
            _scope("libdw1t64", FOUR_HOSTS),
            _scope("libxslt1.1", FOUR_HOSTS),
            _scope("busybox-static", FOUR_HOSTS),
            _scope("busybox-initramfs", FOUR_HOSTS),
            _scope("libarchive13t64", FOUR_HOSTS),
            _scope("tar", FOUR_HOSTS),
            _scope("rsync", FOUR_HOSTS),
            _scope("wget", FOUR_HOSTS),
            _scope("git", FOUR_HOSTS),
            _scope("git-man", FOUR_HOSTS),
        ),
    ),
)


def _build_package_index(
    rules: Sequence[DeviationRule],
) -> dict[str, tuple[DeviationRule, DeviationScope]]:
    """Build an exact package lookup and reject ambiguous rule metadata."""
    out: dict[str, tuple[DeviationRule, DeviationScope]] = {}
    for rule in rules:
        for scope in rule.scopes:
            package = scope.package.casefold()
            if package in out:
                other = out[package][0]
                raise ValueError(
                    f"package {package!r} appears in both {other.dr_id} and {rule.dr_id}"
                )
            out[package] = (rule, scope)
    return out


def _extract_package(title: str) -> str | None:
    """Extract the package from a title shaped as ``CVE-... in package``."""
    match = TITLE_PKG_RE.search(title or "")
    return match.group(1).casefold() if match else None


def _unique_prop(item: dict[str, Any], name: str) -> tuple[str | None, str | None]:
    """Return one normalized property value or an ambiguity error."""
    props = item.get("props", [])
    if not isinstance(props, list):
        return None, "props is not a list"

    values = {
        str(prop.get("value", "")).strip()
        for prop in props
        if isinstance(prop, dict)
        and prop.get("name") == name
        and str(prop.get("value", "")).strip()
    }
    if len(values) > 1:
        return None, f"conflicting {name!r} properties"
    return (next(iter(values)) if values else None), None


def _extract_cve(item: dict[str, Any]) -> tuple[str | None, str | None]:
    """Read a CVE property, with the title as a deterministic fallback."""
    prop_cve, error = _unique_prop(item, "cve")
    if error:
        return None, error

    title_match = TITLE_CVE_RE.search(str(item.get("title", "")))
    title_cve = title_match.group(0).upper() if title_match else None
    normalized_prop = prop_cve.upper() if prop_cve else None
    if normalized_prop and title_cve and normalized_prop != title_cve:
        return None, "cve property conflicts with the CVE in the title"
    return normalized_prop or title_cve, None


def _lifecycle_error(rule: DeviationRule, as_of: date) -> str | None:
    """Return why a rule is ineligible on ``as_of``, or None when active."""
    if rule.status.casefold() != APPROVED_STATUS.casefold():
        return f"status {rule.status!r} is not Approved"
    if as_of < rule.effective_on:
        return f"not effective until {rule.effective_on.isoformat()}"
    if as_of > rule.expires_on:
        return f"expired on {rule.expires_on.isoformat()}"
    return None


def _item_id(item: dict[str, Any]) -> str:
    return str(item.get("uuid") or item.get("title") or "<unidentified item>")


def _violation(
    violations: list[PreflightViolation],
    index: int,
    item: dict[str, Any],
    rule: DeviationRule,
    reason: str,
) -> None:
    violations.append(
        PreflightViolation(
            item_index=index,
            item_id=_item_id(item),
            dr_id=rule.dr_id,
            reason=reason,
        )
    )


def preflight(
    data: dict[str, Any],
    *,
    as_of: date,
    rules: Sequence[DeviationRule] | None = None,
) -> PreflightResult:
    """Build a complete mutation plan without changing ``data``."""
    selected_rules = tuple(DR_RULES if rules is None else rules)
    package_index = _build_package_index(selected_rules)

    try:
        items = data["plan-of-action-and-milestones"]["poam-items"]
    except (KeyError, TypeError) as exc:
        raise ValueError("input is missing OSCAL POA&M poam-items") from exc
    if not isinstance(items, list):
        raise ValueError("OSCAL POA&M poam-items must be a list")

    counters: dict[str, int] = {
        "total": len(items),
        "skipped": 0,
        "no_match": 0,
    }
    for rule in selected_rules:
        counters[rule.dr_id] = 0

    violations: list[PreflightViolation] = []
    mutations: list[PlannedMutation] = []

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"poam-items[{index}] must be an object")

        package = _extract_package(str(item.get("title", "")))
        if not package or package not in package_index:
            counters["no_match"] += 1
            continue

        rule, scope = package_index[package]
        lifecycle_error = _lifecycle_error(rule, as_of)
        if lifecycle_error:
            _violation(violations, index, item, rule, lifecycle_error)
            continue

        host, host_error = _unique_prop(item, "affected-host")
        if host_error:
            _violation(violations, index, item, rule, host_error)
            continue
        if not host:
            _violation(violations, index, item, rule, "missing affected-host scope")
            continue
        if host.casefold() not in scope.hosts:
            allowed = ", ".join(sorted(scope.hosts))
            _violation(
                violations,
                index,
                item,
                rule,
                f"affected-host {host!r} is outside documented scope ({allowed})",
            )
            continue

        if scope.cves is not None:
            cve, cve_error = _extract_cve(item)
            if cve_error:
                _violation(violations, index, item, rule, cve_error)
                continue
            if not cve:
                _violation(violations, index, item, rule, "missing CVE scope")
                continue
            if cve not in scope.cves:
                _violation(
                    violations,
                    index,
                    item,
                    rule,
                    f"CVE {cve!r} is outside the documented CVE scope",
                )
                continue

        existing_state, state_error = _unique_prop(item, "poam-state")
        existing_dr, dr_error = _unique_prop(item, "deviation-request")
        if state_error or dr_error:
            _violation(
                violations,
                index,
                item,
                rule,
                state_error or dr_error or "ambiguous existing disposition",
            )
            continue
        if existing_state == rule.state and existing_dr == rule.dr_id:
            counters["skipped"] += 1
            continue
        if existing_dr is not None or existing_state not in (None, "Open"):
            _violation(
                violations,
                index,
                item,
                rule,
                (
                    f"existing disposition conflicts with {rule.dr_id}: "
                    f"poam-state={existing_state!r}, "
                    f"deviation-request={existing_dr!r}"
                ),
            )
            continue

        mutations.append(PlannedMutation(item_index=index, rule=rule))
        counters[rule.dr_id] += 1

    if violations:
        raise PreflightError(violations)
    return PreflightResult(mutations=tuple(mutations), counters=counters)


def _set_prop(item: dict[str, Any], name: str, value: str) -> bool:
    """Insert or update a property. Return whether the item changed."""
    props = item.setdefault("props", [])
    for prop in props:
        if prop.get("name") == name:
            if prop.get("value") == value:
                return False
            prop["value"] = value
            return True
    props.append({"name": name, "value": value})
    return True


def _write_json_atomic(path: Path, data: dict[str, Any]) -> None:
    """Write JSON to a synced sibling temporary file, then atomically replace ``path``."""
    original_mode = stat.S_IMODE(path.stat().st_mode)
    temporary_path: Path | None = None

    try:
        payload = json.dumps(data, indent=2).encode("utf-8")
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(payload)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        os.chmod(temporary_path, original_mode)
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def apply(
    poam_json_path: Path,
    *,
    as_of: date | None = None,
    rules: Sequence[DeviationRule] | None = None,
) -> dict[str, int]:
    """Apply eligible DR dispositions only after a complete preflight passes."""
    effective_date = as_of or date.today()
    data = json.loads(poam_json_path.read_text(encoding="utf-8"))
    result = preflight(data, as_of=effective_date, rules=rules)

    if result.mutations:
        items = data["plan-of-action-and-milestones"]["poam-items"]
        for mutation in result.mutations:
            item = items[mutation.item_index]
            rule = mutation.rule
            _set_prop(item, "poam-state", rule.state)
            _set_prop(item, "deviation-request", rule.dr_id)
            _set_prop(item, "deviation-rationale", rule.rationale)
        _write_json_atomic(poam_json_path, data)

    return result.counters


def _parse_as_of(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected YYYY-MM-DD") from exc


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--poam-json",
        type=Path,
        default=Path("oscal/poam.json"),
        help="Path to OSCAL POA&M JSON (default: oscal/poam.json)",
    )
    parser.add_argument(
        "--as-of",
        type=_parse_as_of,
        default=date.today(),
        help="Evaluate DR lifecycle on this date (default: today)",
    )
    args = parser.parse_args()

    if not args.poam_json.exists():
        print(f"ERROR: {args.poam_json} not found", file=sys.stderr)
        return 1

    try:
        counters = apply(args.poam_json, as_of=args.as_of)
    except PreflightError as exc:
        print(
            f"ERROR: deviation preflight failed as of {args.as_of.isoformat()}: {exc}",
            file=sys.stderr,
        )
        for violation in exc.violations[:20]:
            print(f"  - {violation.render()}", file=sys.stderr)
        remaining = len(exc.violations) - 20
        if remaining > 0:
            print(f"  - ... and {remaining} more", file=sys.stderr)
        print("POA&M was not written.", file=sys.stderr)
        return 2
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"DR evaluation date:  {args.as_of.isoformat()}")
    print(f"Total POA&M items:   {counters['total']}")
    print(f"No package match:    {counters['no_match']}")
    print(f"Already flipped:     {counters['skipped']}")
    for rule in DR_RULES:
        print(f"Flipped to {rule.state:14s} ({rule.dr_id}): {counters[rule.dr_id]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
