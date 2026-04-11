"""Tests for pipelines.ingest.inventory -- overlay merge + Wazuh → components."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml

from pipelines.common.schemas import InventoryComponent
from pipelines.ingest.inventory import (
    build_components_from_wazuh,
    load_overlay,
    merge_overlay,
)


@pytest.fixture
def overlay_yaml(tmp_path: Path) -> Path:
    p = tmp_path / "overlay.yaml"
    p.write_text(
        yaml.safe_dump(
            {
                "defaults": {
                    "location": "Test Location",
                    "asset_type": "Server",
                },
                "agents": {
                    "brisket": {
                        "asset_tag": "T-001",
                        "function": "Test SIEM",
                        "diagram_label": "S1",
                        "boundary": "in",
                        "is_virtual": False,
                        "hardware_model": "TestModel",
                    },
                    "sear": {
                        "asset_tag": "T-099",
                        "function": "Excluded",
                        "boundary": "out",
                        "is_virtual": False,
                    },
                },
                "non_agent_assets": [
                    {
                        "hostname": "opnsense",
                        "ip": "10.10.10.1",
                        "function": "Firewall",
                        "asset_tag": "F-001",
                        "diagram_label": "F1",
                        "asset_type": "Appliance",
                        "is_virtual": False,
                        "hardware_model": "VP2420",
                        "boundary": "in",
                    }
                ],
                "out_of_boundary": [
                    {"hostname": "DC01", "ip": "10.10.30.40", "reason": "AD"},
                ],
            }
        )
    )
    return p


def _wazuh_mock_with_os_hw() -> MagicMock:
    m = MagicMock()
    m.list_agents.return_value = [
        {"id": "015", "name": "brisket", "ip": "10.10.20.30", "status": "active"},
        {"id": "002", "name": "sear", "ip": "10.10.20.20", "status": "active"},
        {"id": "007", "name": "DC01", "ip": "10.10.30.40", "status": "active"},
    ]
    m.get_syscollector_os.return_value = {
        "os": {"name": "Ubuntu", "version": "24.04.4 LTS (Noble Numbat)"},
        "architecture": "x86_64",
        "release": "6.8.0-107-generic",
    }
    m.get_syscollector_hardware.return_value = {
        "board_serial": "ABC123",
        "cpu": {"name": "i9", "cores": 24},
        "ram": {"total": 64000000},
    }
    return m


def test_load_overlay_returns_parsed_yaml(overlay_yaml: Path) -> None:
    overlay = load_overlay(overlay_yaml)
    assert "brisket" in overlay["agents"]
    assert overlay["agents"]["brisket"]["asset_tag"] == "T-001"
    assert overlay["defaults"]["location"] == "Test Location"


def test_merge_overlay_applies_defaults_without_overriding_explicit() -> None:
    agent_meta = {
        "asset_tag": "X",
        "function": "F",
        "diagram_label": "L",
        "boundary": "in",
        "is_virtual": False,
        "location": "Specific Loc",  # explicit override
    }
    defaults = {"location": "Default Loc", "asset_type": "Server"}
    merged = merge_overlay(agent_meta, defaults)
    assert merged["location"] == "Specific Loc"  # explicit wins
    assert merged["asset_type"] == "Server"  # default applied
    assert merged["asset_tag"] == "X"


def test_build_components_filters_to_in_boundary(overlay_yaml: Path) -> None:
    """brisket (in) included; sear (out) excluded; DC01 (no overlay entry)
    excluded; opnsense (non_agent_assets, in) included."""
    fake_wazuh = _wazuh_mock_with_os_hw()
    components = build_components_from_wazuh(
        fake_wazuh, load_overlay(overlay_yaml)
    )

    hostnames = {c.hostname for c in components}
    assert hostnames == {"brisket", "opnsense"}

    brisket = next(c for c in components if c.hostname == "brisket")
    assert isinstance(brisket, InventoryComponent)
    assert brisket.boundary == "in"
    assert brisket.os_name == "Ubuntu"
    assert brisket.os_version == "24.04.4 LTS (Noble Numbat)"
    assert brisket.patch_level == "6.8.0-107-generic"
    assert brisket.function == "Test SIEM"
    assert brisket.asset_tag == "T-001"
    assert brisket.hardware_model == "TestModel"
    assert brisket.location == "Test Location"  # default applied
    assert brisket.ip_address == "10.10.20.30"
    assert brisket.unique_id == "MSS-HOST-BRISKET"

    opnsense = next(c for c in components if c.hostname == "opnsense")
    assert opnsense.asset_type == "Appliance"
    assert opnsense.authenticated_scan is False  # non-agent
    assert opnsense.unique_id == "MSS-NON-OPNSENSE"


def test_build_components_handles_empty_os_info(overlay_yaml: Path) -> None:
    """Agents with a stale or empty syscollector.os record still produce
    a valid InventoryComponent -- fields fall through to None."""
    fake = MagicMock()
    fake.list_agents.return_value = [
        {"id": "015", "name": "brisket", "ip": "10.10.20.30", "status": "active"},
    ]
    fake.get_syscollector_os.return_value = {}
    fake.get_syscollector_hardware.return_value = {}

    components = build_components_from_wazuh(fake, load_overlay(overlay_yaml))
    brisket = next(c for c in components if c.hostname == "brisket")
    assert brisket.os_name is None
    assert brisket.os_version is None
    assert brisket.patch_level is None
    # software_vendor falls back to None rather than raising on empty string
    assert brisket.software_vendor is None


def test_build_components_excludes_out_of_boundary_agents(
    overlay_yaml: Path,
) -> None:
    fake = _wazuh_mock_with_os_hw()
    components = build_components_from_wazuh(fake, load_overlay(overlay_yaml))
    assert all(c.boundary == "in" for c in components)
    assert not any(c.hostname == "sear" for c in components)


def test_build_components_skips_unknown_agents(overlay_yaml: Path) -> None:
    """DC01 has no overlay entry -- treated as out-of-boundary and excluded."""
    fake = _wazuh_mock_with_os_hw()
    components = build_components_from_wazuh(fake, load_overlay(overlay_yaml))
    assert not any(c.hostname == "DC01" for c in components)
