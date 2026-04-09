"""Unified Click-based CLI entry point for the FedRAMP Low ConMon pipelines.

This module is invoked by ``pipelines.sh`` through a passthrough arm
(per ADR 0006 Deviation 2) so every pipeline command shares the Plan 1
``pipelines.sh help|install|smoke|...`` entry surface. The Makefile
remains a thin alias that forwards targets to ``pipelines.sh`` for
POSIX systems that still expect ``make``.

Commands
--------

``inventory``
    Pull Wazuh agents + overlay -> InventoryComponent list ->
    ``oscal/component-definition.json``.

``render-iiw``
    ``oscal/component-definition.json`` -> ``inventory/IIW-<YYYY-MM>.xlsx``.

``ingest-findings``
    Pull Wazuh vulnerability hits -> normalized Findings -> push to
    DefectDojo, grouped by product, into the per-month ConMon
    engagement (auto-created if missing).

``build-poam``
    Pull DefectDojo findings -> ``oscal/poam.json``.

``render-poam``
    ``oscal/poam.json`` -> ``poam/POAM-<YYYY-MM>.xlsx``.

``oscal``
    Composite: inventory + build-poam.

``conmon``
    Full monthly cycle: ingest-findings + oscal + render-iiw + render-poam.

The ``HOST_TO_PRODUCT`` map uses ASCII hyphens per ADR 0006 amendment
2026-04-09 — the DefectDojo seed script in Plan 1 created the
products with ``-``, not em dashes. It includes the ``opnsense``
non-agent entry so a future SCA or firewall-audit source can route
findings to product id=4 without another code change.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import click

from pipelines.build.oscal_component import build_component_definition
from pipelines.build.oscal_poam import build_poam_from_defectdojo
from pipelines.build.oscal_ssp import assemble_ssp
from pipelines.common.config import load_config
from pipelines.common.defectdojo import DefectDojoClient
from pipelines.common.logging import get_logger
from pipelines.common.wazuh import WazuhClient
from pipelines.common.wazuh_indexer import WazuhIndexerClient
from pipelines.ingest.inventory import build_components_from_wazuh, load_overlay
from pipelines.ingest.wazuh_vulns import ingest_wazuh_vulns
from pipelines.push.defectdojo import push_findings_to_defectdojo
from pipelines.render.iiw import render_iiw_from_oscal
from pipelines.render.poam import render_poam_from_oscal


logger = get_logger("pipelines.cli")


# ASCII hyphens per ADR 0006 amendment 2026-04-09.
# 5 products in DefectDojo. dojo + regscale share one product, so two
# hostnames both map to "MSS GRC Tooling - dojo + regscale".
HOST_TO_PRODUCT: dict[str, str] = {
    "brisket": "MSS Core - brisket",
    "haccp": "MSS Log Analytics - haccp",
    "smokehouse": "MSS Network Sensors - smokehouse",
    "dojo": "MSS GRC Tooling - dojo + regscale",
    "regscale": "MSS GRC Tooling - dojo + regscale",
    "opnsense": "MSS Boundary Protection - OPNsense",
}

IN_BOUNDARY_WAZUH_AGENTS: tuple[str, ...] = (
    "brisket",
    "haccp",
    "smokehouse",
    "dojo",
    "regscale",
)

# Conventional artifact paths relative to the repo root.
OSCAL_COMPONENT_DEF = Path("oscal/component-definition.json")
OSCAL_POAM = Path("oscal/poam.json")
OSCAL_SSP = Path("oscal/ssp.json")
OVERLAY_PATH = Path("inventory/overlay.yaml")
IIW_TEMPLATE = Path("templates/FedRAMP-IIW-Template-Rev5.xlsx")
POAM_TEMPLATE = Path("templates/FedRAMP-POAM-Template-Rev5.xlsx")
TRESTLE_WORKSPACE = Path("trestle-workspace")
SSP_NAME = "mss-ssp"


def _current_month() -> str:
    return date.today().strftime("%Y-%m")


def _engagement_name() -> str:
    return f"ConMon {_current_month()}"


@click.group()
def cli() -> None:
    """FedRAMP homelab ConMon pipelines."""


# --- inventory / render-iiw -----------------------------------------------


@cli.command()
def inventory() -> None:
    """Ingest Wazuh inventory -> OSCAL component-definition JSON."""
    cfg = load_config()
    wazuh = WazuhClient(
        cfg.wazuh_api_url,
        cfg.wazuh_api_user,
        cfg.wazuh_api_password,
        verify=False,
    )
    overlay = load_overlay(OVERLAY_PATH)
    components = build_components_from_wazuh(wazuh, overlay)
    build_component_definition(components, OSCAL_COMPONENT_DEF)
    click.echo(f"OK: {len(components)} in-boundary components -> {OSCAL_COMPONENT_DEF}")


@cli.command("render-iiw")
def render_iiw() -> None:
    """Render IIW xlsx from OSCAL component-definition JSON."""
    out = Path(f"inventory/IIW-{_current_month()}.xlsx")
    render_iiw_from_oscal(
        component_def_path=OSCAL_COMPONENT_DEF,
        template_path=IIW_TEMPLATE,
        output_path=out,
    )
    click.echo(f"OK: wrote {out}")


# --- ingest-findings (Wazuh indexer -> DefectDojo) ------------------------


@cli.command("ingest-findings")
def ingest_findings() -> None:
    """Ingest Wazuh vulnerability hits -> push to DefectDojo."""
    cfg = load_config()
    indexer = WazuhIndexerClient(
        cfg.wazuh_indexer_url,
        cfg.wazuh_indexer_user,
        cfg.wazuh_indexer_password,
        verify=False,
    )
    findings = ingest_wazuh_vulns(indexer, IN_BOUNDARY_WAZUH_AGENTS)
    click.echo(f"Ingested {len(findings)} findings from Wazuh indexer")

    dd = DefectDojoClient(cfg.defectdojo_url, cfg.defectdojo_api_key)
    result = push_findings_to_defectdojo(
        client=dd,
        findings=findings,
        host_to_product=HOST_TO_PRODUCT,
        engagement_name=_engagement_name(),
    )
    click.echo(f"OK: imported={result['imported']} skipped={result['skipped']}")


# --- build-poam / render-poam --------------------------------------------


@cli.command("build-poam")
def build_poam() -> None:
    """Pull DefectDojo findings -> OSCAL POA&M JSON."""
    cfg = load_config()
    dd = DefectDojoClient(cfg.defectdojo_url, cfg.defectdojo_api_key)
    findings = dd.list_findings()
    click.echo(f"Pulled {len(findings)} findings from DefectDojo")
    build_poam_from_defectdojo(findings=findings, output_path=OSCAL_POAM)
    click.echo(f"OK: {OSCAL_POAM}")


@cli.command("render-poam")
def render_poam() -> None:
    """Render POA&M xlsx from OSCAL POA&M JSON."""
    out = Path(f"poam/POAM-{_current_month()}.xlsx")
    render_poam_from_oscal(
        oscal_poam_path=OSCAL_POAM,
        template_path=POAM_TEMPLATE,
        output_path=out,
    )
    click.echo(f"OK: wrote {out}")


# --- SSP assembly (Plan 3 prep) ------------------------------------------


@cli.command("ssp-assemble")
def ssp_assemble() -> None:
    """Run trestle author ssp-assemble against the markdown scaffold.

    Plan 2 wires the assembly path without filling the 156 control
    markdown files — running this against the empty scaffold is
    expected to either produce a minimal SSP or fail with a Trestle
    diagnostic that tells Plan 3 exactly which controls need prose.
    """
    assemble_ssp(
        ssp_name=SSP_NAME,
        workspace=TRESTLE_WORKSPACE,
        output_path=OSCAL_SSP,
    )
    click.echo(f"OK: wrote {OSCAL_SSP}")


# --- composite stages ----------------------------------------------------


@cli.command()
@click.pass_context
def oscal(ctx: click.Context) -> None:
    """Composite: inventory + build-poam. Rebuild the OSCAL source of truth."""
    ctx.invoke(inventory)
    ctx.invoke(build_poam)
    click.echo("OK: oscal composite complete")


@cli.command()
@click.pass_context
def conmon(ctx: click.Context) -> None:
    """Full monthly cycle: ingest-findings + oscal + render-iiw + render-poam."""
    ctx.invoke(ingest_findings)
    ctx.invoke(inventory)
    ctx.invoke(build_poam)
    ctx.invoke(render_iiw)
    ctx.invoke(render_poam)
    click.echo("OK: monthly ConMon cycle complete")


if __name__ == "__main__":
    cli()
