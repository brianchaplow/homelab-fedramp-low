"""Inventory ingestion: Wazuh syscollector → InventoryComponent list.

Pulls every active agent from the Wazuh API, joins each one with the
static overlay YAML at ``inventory/overlay.yaml``, and emits a list of
:class:`pipelines.common.schemas.InventoryComponent` records for
everything tagged ``boundary: in``. Also adds any non-Wazuh-managed
in-boundary assets (firewall, switch) from the overlay's
``non_agent_assets`` section so the IIW asset count is complete.

Why a name-keyed overlay instead of an id-keyed one: per ADR 0006
Deviation 6, Wazuh agent ids drift with enrollment order (haccp was
014 before the 2026-04 rack build, dojo is 016 after). Names are
stable across reenrollments so the overlay file does not need a diff
every time an agent is re-registered.

Fields like kernel release, CPU model, RAM size live under different
paths in the live Wazuh syscollector response than the plan text
originally hinted (``release`` at top-level, not ``os.kernel``). This
module uses the live shape — live probe 2026-04-09 — not the plan
text's guess.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from pipelines.common.logging import get_logger
from pipelines.common.schemas import InventoryComponent
from pipelines.common.wazuh import WazuhClient


logger = get_logger(__name__)


def load_overlay(path: Path) -> dict[str, Any]:
    """Load and return the inventory overlay YAML."""
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def merge_overlay(
    agent_meta: dict[str, Any], defaults: dict[str, Any]
) -> dict[str, Any]:
    """Return a new dict: defaults first, then agent_meta overrides.

    Explicit values in ``agent_meta`` always win over ``defaults``. Keys
    that are only in ``defaults`` are applied to the result.
    """
    merged: dict[str, Any] = dict(defaults)
    merged.update(agent_meta)
    return merged


def _first_word_or_none(value: str | None) -> str | None:
    """Return the first whitespace-delimited word, or ``None`` on empty."""
    if not value:
        return None
    parts = value.split()
    return parts[0] if parts else None


def _software_name(os_block: dict[str, Any]) -> str | None:
    name = os_block.get("name") or ""
    version = os_block.get("version") or ""
    combined = f"{name} {version}".strip()
    return combined or None


def build_components_from_wazuh(
    client: WazuhClient,
    overlay: dict[str, Any],
) -> list[InventoryComponent]:
    """Build normalized InventoryComponent records from live Wazuh data.

    Agents matching a ``boundary: in`` overlay entry are pulled with
    syscollector OS + hardware and emitted as ``MSS-HOST-<NAME>``.
    Agents without an overlay entry are silently skipped (treated as
    out-of-boundary). ``non_agent_assets`` marked ``boundary: in`` are
    emitted as ``MSS-NON-<NAME>`` with ``authenticated_scan=False``.
    """
    defaults = overlay.get("defaults", {}) or {}
    agent_overlays = overlay.get("agents", {}) or {}
    components: list[InventoryComponent] = []

    agents = client.list_agents(status="active")
    logger.info("fetched %d active agents from Wazuh", len(agents))

    for agent in agents:
        name = agent.get("name")
        if not name or name not in agent_overlays:
            logger.debug(
                "skipping agent %s — no overlay entry, treated as out-of-boundary",
                name,
            )
            continue

        meta = merge_overlay(agent_overlays[name], defaults)
        if meta.get("boundary") != "in":
            logger.debug("skipping agent %s — overlay marks it out-of-boundary", name)
            continue

        os_info = client.get_syscollector_os(agent["id"]) or {}
        _hw_info = client.get_syscollector_hardware(agent["id"]) or {}

        os_block: dict[str, Any] = os_info.get("os") or {}
        os_name = os_block.get("name")
        os_version = os_block.get("version")
        # Kernel release is at the top level of syscollector/os, not under
        # os.kernel. Verified via live probe 2026-04-09.
        patch_level = os_info.get("release") or os_block.get("kernel")

        components.append(
            InventoryComponent(
                unique_id=f"MSS-HOST-{name.upper()}",
                hostname=name,
                ip_address=agent.get("ip", ""),
                mac_address=os_info.get("mac"),
                is_virtual=meta.get("is_virtual", False),
                netbios_name=name,
                os_name=os_name,
                os_version=os_version,
                location=meta.get("location"),
                asset_type=meta.get("asset_type", "Server"),
                hardware_model=meta.get("hardware_model"),
                software_vendor=_first_word_or_none(os_name),
                software_name=_software_name(os_block),
                patch_level=patch_level,
                diagram_label=meta.get("diagram_label"),
                function=meta.get("function", "Unknown"),
                asset_tag=meta.get("asset_tag"),
                end_of_life=meta.get("end_of_life"),
                boundary="in",
                comments=meta.get("comments", ""),
            )
        )
        logger.info("added in-boundary agent component: %s", name)

    # Non-Wazuh-managed in-boundary assets (firewall, switch)
    for non_agent in overlay.get("non_agent_assets", []) or []:
        if non_agent.get("boundary") != "in":
            continue
        meta = merge_overlay(non_agent, defaults)
        components.append(
            InventoryComponent(
                unique_id=f"MSS-NON-{non_agent['hostname'].upper()}",
                hostname=non_agent["hostname"],
                ip_address=non_agent["ip"],
                is_virtual=meta.get("is_virtual", False),
                asset_type=meta.get("asset_type", "Appliance"),
                location=meta.get("location"),
                hardware_model=meta.get("hardware_model"),
                diagram_label=meta.get("diagram_label"),
                function=meta.get("function", "Unknown"),
                asset_tag=meta.get("asset_tag"),
                authenticated_scan=False,
                boundary="in",
                comments=meta.get("comments", "non-Wazuh-managed asset"),
            )
        )
        logger.info("added non-agent component: %s", non_agent["hostname"])

    logger.info("built %d in-boundary inventory components total", len(components))
    return components
