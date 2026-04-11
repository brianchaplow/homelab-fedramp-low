"""Tests for pipelines.push.regscale -- best-effort OSCAL push."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pipelines.push.regscale import (
    MANUAL_RUNBOOK_PATH,
    OSCAL_IMPORT_PATHS,
    push_oscal_to_regscale,
)


@pytest.fixture
def sample_oscal(tmp_path: Path) -> Path:
    p = tmp_path / "ssp.json"
    p.write_text(
        json.dumps(
            {
                "system-security-plan": {
                    "uuid": "11111111-1111-1111-1111-111111111111",
                    "metadata": {"title": "Test"},
                }
            }
        )
    )
    return p


def _mock_client_with_validation_ok() -> MagicMock:
    c = MagicMock()
    c.post.return_value = {"valid": True}
    return c


def test_push_oscal_returns_manual_required_when_no_import_path(
    sample_oscal: Path,
) -> None:
    """Current reality: CE has no generic OSCAL import API, so every
    push returns manual-required plus runbook + validation note."""
    assert OSCAL_IMPORT_PATHS == {}  # baseline assumption
    client = _mock_client_with_validation_ok()
    result = push_oscal_to_regscale(client, sample_oscal, "ssp")
    assert result["status"] == "manual-required"
    assert result["runbook"] == str(MANUAL_RUNBOOK_PATH)
    assert "validated" in result["validation"]
    assert result["oscal_type"] == "ssp"


def test_push_oscal_reports_validation_skip_when_endpoint_unavailable(
    sample_oscal: Path,
) -> None:
    """If the ValidateFedRAMP endpoint errors, the push still returns
    manual-required -- validation is a nice-to-have, not a gate."""
    client = MagicMock()
    client.post.side_effect = Exception("500 Server Error")
    result = push_oscal_to_regscale(client, sample_oscal, "poam")
    assert result["status"] == "manual-required"
    assert "validation skipped" in result["validation"]


def test_push_oscal_errors_on_missing_file(tmp_path: Path) -> None:
    client = _mock_client_with_validation_ok()
    missing = tmp_path / "nope.json"
    result = push_oscal_to_regscale(client, missing, "ssp")
    assert result["status"] == "error"
    assert "not found" in result["body"]


def test_push_oscal_uses_import_path_when_populated(
    sample_oscal: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When RegScale CE eventually exposes a generic import endpoint,
    populating OSCAL_IMPORT_PATHS at runtime switches the push from
    manual-required to a real POST. The push pipeline calls post()
    twice: once for the best-effort validation, once for the import."""
    monkeypatch.setitem(OSCAL_IMPORT_PATHS, "ssp", "/api/oscal/ssp")
    client = MagicMock()
    client.post.return_value = {"id": 42}
    result = push_oscal_to_regscale(client, sample_oscal, "ssp")
    assert result["status"] == "ok"
    assert result["regscale_id"] == 42
    # Two post() calls: validation + import. The last one is the import.
    assert client.post.call_count == 2
    last_call = client.post.call_args_list[-1]
    assert last_call.args[0] == "/api/oscal/ssp"


def test_manual_runbook_exists() -> None:
    """The manual-required fallback references a real file in the repo."""
    assert Path("runbooks/regscale-manual-import.md").exists()
