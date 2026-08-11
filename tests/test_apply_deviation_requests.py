"""Focused tests for the fail-closed Deviation Request applicator."""
from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path
from types import ModuleType

import pytest


def _load_module() -> ModuleType:
    path = Path(__file__).parents[1] / "runbooks" / "apply-deviation-requests.py"
    spec = importlib.util.spec_from_file_location("apply_deviation_requests", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


dr = _load_module()


def _item(
    title: str,
    *,
    host: str | None = "brisket",
    cve: str | None = None,
    state: str = "Open",
    deviation_request: str | None = None,
) -> dict:
    props = [{"name": "poam-state", "value": state}]
    if host is not None:
        props.append({"name": "affected-host", "value": host})
    if cve is not None:
        props.append({"name": "cve", "value": cve})
    if deviation_request is not None:
        props.append({"name": "deviation-request", "value": deviation_request})
    return {"uuid": f"item-{abs(hash((title, host, cve)))}", "title": title, "props": props}


def _write_poam(path: Path, items: list[dict]) -> bytes:
    data = {"plan-of-action-and-milestones": {"poam-items": items}}
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path.read_bytes()


def _props(item: dict) -> dict[str, str]:
    return {prop["name"]: prop["value"] for prop in item["props"]}


def _items(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))[
        "plan-of-action-and-milestones"
    ]["poam-items"]


def test_rule_metadata_matches_current_dr_documents() -> None:
    rules = {rule.dr_id: rule for rule in dr.DR_RULES}

    assert set(rules) == {"FP-0002", "FP-0003", "OR-0002"}
    assert all(rule.status == "Approved" for rule in rules.values())
    assert all(rule.effective_on == date(2026, 5, 4) for rule in rules.values())
    assert rules["FP-0002"].expires_on == date(2027, 5, 4)
    assert rules["FP-0003"].expires_on == date(2026, 8, 4)
    assert rules["OR-0002"].expires_on == date(2026, 8, 4)

    fp2 = {scope.package: scope for scope in rules["FP-0002"].scopes}
    assert fp2["libde265-0"].hosts == frozenset({"brisket", "haccp"})
    assert fp2["libavahi-client3"].hosts == frozenset({"brisket"})

    fp3_scope = rules["FP-0003"].scopes[0]
    assert fp3_scope.hosts == frozenset({"dojo", "regscale"})
    assert fp3_scope.cves == frozenset(dr.FP_0003_CVES)
    assert len(fp3_scope.cves) == 12


def test_active_rules_apply_only_after_complete_preflight(tmp_path: Path) -> None:
    path = tmp_path / "poam.json"
    _write_poam(
        path,
        [
            _item("CVE-2025-1000 in Libde265-0", host="brisket"),
            _item("CVE-2020-13791 in qemu-guest-agent", host="dojo"),
            _item("CVE-2025-2000 in Binutils", host="haccp"),
        ],
    )

    counters = dr.apply(path, as_of=date(2026, 6, 1))
    items = _items(path)

    assert counters["FP-0002"] == 1
    assert counters["FP-0003"] == 1
    assert counters["OR-0002"] == 1
    assert _props(items[0])["deviation-request"] == "FP-0002"
    assert _props(items[1])["deviation-request"] == "FP-0003"
    assert _props(items[2])["deviation-request"] == "OR-0002"

    before_second_run = path.read_bytes()
    second = dr.apply(path, as_of=date(2026, 6, 1))
    assert second["skipped"] == 3
    assert path.read_bytes() == before_second_run


def test_expired_rules_abort_entire_write_on_2026_08_10(tmp_path: Path) -> None:
    path = tmp_path / "poam.json"
    original = _write_poam(
        path,
        [
            _item("CVE-2025-1000 in Libde265-0", host="brisket"),
            _item("CVE-2020-13791 in qemu-guest-agent", host="dojo"),
            _item("CVE-2025-2000 in Binutils", host="haccp"),
        ],
    )

    with pytest.raises(dr.PreflightError) as exc_info:
        dr.apply(path, as_of=date(2026, 8, 10))

    rendered = "\n".join(v.render() for v in exc_info.value.violations)
    assert "FP-0003" in rendered
    assert "OR-0002" in rendered
    assert "expired on 2026-08-04" in rendered
    assert path.read_bytes() == original


def test_unapproved_status_aborts_without_writing(tmp_path: Path) -> None:
    path = tmp_path / "poam.json"
    original = _write_poam(
        path,
        [_item("CVE-2025-1000 in Libde265-0", host="brisket")],
    )
    fp2 = next(rule for rule in dr.DR_RULES if rule.dr_id == "FP-0002")
    submitted = replace(fp2, status="Submitted")

    with pytest.raises(dr.PreflightError, match="preflight violation") as exc_info:
        dr.apply(path, as_of=date(2026, 6, 1), rules=(submitted,))

    assert "not Approved" in exc_info.value.violations[0].reason
    assert path.read_bytes() == original


def test_not_yet_effective_rule_aborts_without_writing(tmp_path: Path) -> None:
    path = tmp_path / "poam.json"
    original = _write_poam(
        path,
        [_item("CVE-2025-1000 in Libde265-0", host="brisket")],
    )

    with pytest.raises(dr.PreflightError) as exc_info:
        dr.apply(path, as_of=date(2026, 5, 3))

    assert "not effective until 2026-05-04" in exc_info.value.violations[0].reason
    assert path.read_bytes() == original


def test_out_of_scope_host_aborts_before_valid_item_is_written(tmp_path: Path) -> None:
    path = tmp_path / "poam.json"
    original = _write_poam(
        path,
        [
            _item("CVE-2025-1000 in Libde265-0", host="brisket"),
            _item("CVE-2025-1001 in Libde265-0", host="dojo"),
        ],
    )

    with pytest.raises(dr.PreflightError) as exc_info:
        dr.apply(path, as_of=date(2026, 6, 1))

    assert "outside documented scope" in exc_info.value.violations[0].reason
    assert path.read_bytes() == original


def test_missing_host_aborts_before_valid_item_is_written(tmp_path: Path) -> None:
    path = tmp_path / "poam.json"
    original = _write_poam(
        path,
        [
            _item("CVE-2025-1000 in Libde265-0", host="brisket"),
            _item("CVE-2025-1001 in Libde265-0", host=None),
        ],
    )

    with pytest.raises(dr.PreflightError) as exc_info:
        dr.apply(path, as_of=date(2026, 6, 1))

    assert "missing affected-host scope" in exc_info.value.violations[0].reason
    assert path.read_bytes() == original


@pytest.mark.parametrize(
    ("state", "deviation_request"),
    [
        ("Closed", None),
        ("Open", "MANUAL-0001"),
        ("False Positive", None),
        ("Open", "FP-0002"),
    ],
)
def test_existing_disposition_conflict_aborts_without_writing(
    tmp_path: Path,
    state: str,
    deviation_request: str | None,
) -> None:
    path = tmp_path / "poam.json"
    original = _write_poam(
        path,
        [
            _item("CVE-2025-1000 in Libde265-0", host="brisket"),
            _item(
                "CVE-2025-1001 in Libde265-0",
                host="brisket",
                state=state,
                deviation_request=deviation_request,
            ),
        ],
    )

    with pytest.raises(dr.PreflightError) as exc_info:
        dr.apply(path, as_of=date(2026, 6, 1))

    assert "existing disposition conflicts with FP-0002" in (
        exc_info.value.violations[0].reason
    )
    assert path.read_bytes() == original


def test_atomic_replace_failure_preserves_original_and_removes_temp_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "poam.json"
    original = _write_poam(
        path,
        [_item("CVE-2025-1000 in Libde265-0", host="brisket")],
    )
    replacement_source: Path | None = None

    def fail_replace(source: Path, destination: Path) -> None:
        nonlocal replacement_source
        replacement_source = Path(source)
        assert replacement_source.parent == path.parent
        assert Path(destination) == path
        raise OSError("simulated atomic replace failure")

    monkeypatch.setattr(dr.os, "replace", fail_replace)

    with pytest.raises(OSError, match="simulated atomic replace failure"):
        dr.apply(path, as_of=date(2026, 6, 1))

    assert replacement_source is not None
    assert not replacement_source.exists()
    assert path.read_bytes() == original


@pytest.mark.parametrize(
    ("title", "expected_reason"),
    [
        ("Finding in qemu-guest-agent", "missing CVE scope"),
        (
            "CVE-2099-9999 in qemu-guest-agent",
            "outside the documented CVE scope",
        ),
    ],
)
def test_fp0003_cve_scope_is_fail_closed(
    tmp_path: Path,
    title: str,
    expected_reason: str,
) -> None:
    path = tmp_path / "poam.json"
    original = _write_poam(
        path,
        [
            _item("CVE-2025-1000 in Libde265-0", host="brisket"),
            _item(title, host="dojo"),
        ],
    )

    with pytest.raises(dr.PreflightError) as exc_info:
        dr.apply(path, as_of=date(2026, 6, 1))

    assert expected_reason in exc_info.value.violations[0].reason
    assert path.read_bytes() == original


def test_expiration_date_is_inclusive(tmp_path: Path) -> None:
    path = tmp_path / "poam.json"
    _write_poam(
        path,
        [_item("CVE-2024-8612 in qemu-guest-agent", host="regscale")],
    )

    counters = dr.apply(path, as_of=date(2026, 8, 4))

    assert counters["FP-0003"] == 1
    assert _props(_items(path)[0])["deviation-request"] == "FP-0003"


def test_cli_accepts_deterministic_as_of(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    path = tmp_path / "poam.json"
    _write_poam(
        path,
        [_item("CVE-2025-1000 in Libde265-0", host="brisket")],
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "apply-deviation-requests.py",
            "--poam-json",
            str(path),
            "--as-of",
            "2026-06-01",
        ],
    )

    assert dr.main() == 0
    assert "DR evaluation date:  2026-06-01" in capsys.readouterr().out
