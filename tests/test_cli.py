"""Tests for pipelines.cli -- Click app surface area.

These tests exercise the Click command tree via CliRunner without
actually hitting Wazuh or DefectDojo. The full end-to-end run is
covered by Task 14 Step 4's live smoke.
"""
from __future__ import annotations

from click.testing import CliRunner

from pipelines.cli import HOST_TO_PRODUCT, IN_BOUNDARY_WAZUH_AGENTS, cli


def test_cli_help_lists_every_subcommand() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    for command in (
        "inventory",
        "render-iiw",
        "ingest-findings",
        "build-poam",
        "render-poam",
        "oscal",
        "conmon",
    ):
        assert command in result.output


def test_host_to_product_uses_ascii_hyphens_and_has_six_entries() -> None:
    """Per ADR 0006 amendment 2026-04-09: ASCII hyphen, not em dash,
    and 6 host entries (5 Wazuh agents + opnsense non-agent)."""
    assert len(HOST_TO_PRODUCT) == 6
    for product in HOST_TO_PRODUCT.values():
        # No em dash anywhere (U+2014)
        assert "\u2014" not in product
        assert "-" in product
    # Required mappings
    assert HOST_TO_PRODUCT["brisket"] == "MSS Core - brisket"
    assert HOST_TO_PRODUCT["haccp"] == "MSS Log Analytics - haccp"
    assert HOST_TO_PRODUCT["smokehouse"] == "MSS Network Sensors - smokehouse"
    assert HOST_TO_PRODUCT["dojo"] == "MSS GRC Tooling - dojo + regscale"
    assert HOST_TO_PRODUCT["regscale"] == "MSS GRC Tooling - dojo + regscale"
    assert HOST_TO_PRODUCT["opnsense"] == "MSS Boundary Protection - OPNsense"


def test_in_boundary_wazuh_agents_excludes_opnsense() -> None:
    """opnsense has an inventory entry but is not a Wazuh agent, so it
    must not appear in the vuln-ingest loop's agent list."""
    assert "opnsense" not in IN_BOUNDARY_WAZUH_AGENTS
    assert set(IN_BOUNDARY_WAZUH_AGENTS) == {
        "brisket",
        "haccp",
        "smokehouse",
        "dojo",
        "regscale",
    }


def test_inventory_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["inventory", "--help"])
    assert result.exit_code == 0
    assert "component-definition" in result.output.lower()


def test_render_iiw_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["render-iiw", "--help"])
    assert result.exit_code == 0
    assert "iiw" in result.output.lower()


def test_ingest_findings_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["ingest-findings", "--help"])
    assert result.exit_code == 0
    assert "defectdojo" in result.output.lower()


def test_conmon_help_documents_full_cycle() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["conmon", "--help"])
    assert result.exit_code == 0
    assert "cycle" in result.output.lower()
