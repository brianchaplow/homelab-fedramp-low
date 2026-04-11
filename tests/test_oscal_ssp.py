"""Tests for pipelines.build.oscal_ssp -- Trestle ssp-assemble wrapper."""
from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pipelines.build.oscal_ssp import assemble_ssp, build_ssp_assemble_cmd


def test_build_ssp_assemble_cmd_uses_top_level_markdown_dir() -> None:
    """Per ADR 0006 Amendment Task 4: Trestle 4.0.1 writes the markdown
    scaffold to ``trestle-workspace/<ssp_name>/`` (top-level), so the
    ``-m`` flag must reference the top-level dir name, not a nested
    ``system-security-plans/<ssp_name>`` path."""
    cmd = build_ssp_assemble_cmd(ssp_name="mss-ssp")
    assert cmd[0].endswith("trestle") or cmd[0] == "trestle"
    assert "author" in cmd
    assert "ssp-assemble" in cmd
    assert "-m" in cmd
    m_idx = cmd.index("-m")
    assert cmd[m_idx + 1] == "mss-ssp"
    assert "-o" in cmd
    o_idx = cmd.index("-o")
    assert cmd[o_idx + 1] == "mss-ssp"


def test_build_ssp_assemble_cmd_includes_compdefs_when_requested() -> None:
    cmd = build_ssp_assemble_cmd(
        ssp_name="mss-ssp",
        component_defs=["mss-inventory"],
    )
    assert "-cd" in cmd
    cd_idx = cmd.index("-cd")
    assert cmd[cd_idx + 1] == "mss-inventory"


@patch("pipelines.build.oscal_ssp.subprocess.run")
def test_assemble_ssp_invokes_trestle_in_workspace(
    mock_run, tmp_path: Path
) -> None:
    workspace = tmp_path / "trestle-workspace"
    workspace.mkdir()
    # Pre-create the assembled output Trestle is expected to produce
    assembled_dir = workspace / "system-security-plans" / "mss-ssp"
    assembled_dir.mkdir(parents=True)
    (assembled_dir / "system-security-plan.json").write_text(
        '{"system-security-plan": {}}', encoding="utf-8"
    )
    output = tmp_path / "ssp-copy.json"
    mock_run.return_value = MagicMock(returncode=0, stdout="OK", stderr="")

    result = assemble_ssp(
        ssp_name="mss-ssp",
        workspace=workspace,
        output_path=output,
    )

    assert result == output
    assert output.exists()
    mock_run.assert_called_once()
    call_kwargs = mock_run.call_args.kwargs
    assert call_kwargs["cwd"] == workspace
    cmd = mock_run.call_args.args[0]
    assert "ssp-assemble" in cmd


@patch("pipelines.build.oscal_ssp.subprocess.run")
def test_assemble_ssp_raises_if_trestle_fails(mock_run, tmp_path: Path) -> None:
    workspace = tmp_path / "trestle-workspace"
    workspace.mkdir()
    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1,
        cmd=["trestle", "author", "ssp-assemble"],
        stderr="missing control prose",
    )
    with pytest.raises(subprocess.CalledProcessError):
        assemble_ssp(
            ssp_name="mss-ssp",
            workspace=workspace,
            output_path=tmp_path / "out.json",
        )


@patch("pipelines.build.oscal_ssp.subprocess.run")
def test_assemble_ssp_raises_when_output_not_produced(
    mock_run, tmp_path: Path
) -> None:
    """If Trestle returns 0 but no JSON file was written, surface a
    FileNotFoundError rather than silently returning a nonexistent
    path to the caller."""
    workspace = tmp_path / "trestle-workspace"
    workspace.mkdir()
    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

    with pytest.raises(FileNotFoundError, match="did not produce SSP"):
        assemble_ssp(
            ssp_name="mss-ssp",
            workspace=workspace,
            output_path=tmp_path / "out.json",
        )
