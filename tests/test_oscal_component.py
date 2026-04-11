"""Tests for pipelines.build.oscal_component -- OSCAL component-definition builder."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from pipelines.build.oscal_component import (
    OSCAL_VERSION,
    build_component_definition,
)
from pipelines.common.schemas import InventoryComponent


UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)
ISO_TZ_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[+-]\d{2}:\d{2}|Z)$"
)


@pytest.fixture
def sample_components() -> list[InventoryComponent]:
    return [
        InventoryComponent(
            unique_id="MSS-HOST-BRISKET",
            hostname="brisket",
            ip_address="10.10.20.30",
            is_virtual=False,
            asset_type="Server",
            os_name="Ubuntu",
            os_version="24.04",
            hardware_model="Lenovo ThinkStation",
            function="SIEM Manager",
            asset_tag="HOMELAB-001",
            diagram_label="S1",
        ),
        InventoryComponent(
            unique_id="MSS-HOST-DOJO",
            hostname="dojo",
            ip_address="10.10.30.27",
            is_virtual=True,
            asset_type="Server",
            os_name="Ubuntu",
            os_version="24.04",
            function="Vulnerability Management",
            asset_tag="HOMELAB-004",
            diagram_label="S4",
        ),
        InventoryComponent(
            unique_id="MSS-NON-OPNSENSE",
            hostname="opnsense",
            ip_address="10.10.10.1",
            is_virtual=False,
            asset_type="Appliance",
            function="Boundary Firewall",
            asset_tag="HOMELAB-FW-001",
            authenticated_scan=False,
        ),
        InventoryComponent(
            unique_id="MSS-NON-MOKERLINK",
            hostname="mokerlink",
            ip_address="10.10.10.2",
            is_virtual=False,
            asset_type="Network",
            function="Microsegmentation Switch",
            authenticated_scan=False,
        ),
    ]


def test_build_component_definition_writes_file(
    sample_components, tmp_path: Path
) -> None:
    out = tmp_path / "cd.json"
    path = build_component_definition(
        components=sample_components,
        output_path=out,
        title="Managed SOC Service",
        version="0.1.0",
    )
    assert path == out
    assert out.exists()


def test_build_component_definition_top_level_shape(
    sample_components, tmp_path: Path
) -> None:
    out = tmp_path / "cd.json"
    build_component_definition(sample_components, out, "Managed SOC Service", "0.1.0")
    data = json.loads(out.read_text(encoding="utf-8"))

    assert "component-definition" in data
    cd = data["component-definition"]
    assert UUID_RE.match(cd["uuid"])
    assert cd["metadata"]["title"] == "Managed SOC Service"
    assert cd["metadata"]["version"] == "0.1.0"
    assert cd["metadata"]["oscal-version"] == OSCAL_VERSION
    assert UUID_RE.match(cd["metadata"]["last-modified"]) is None  # not a uuid
    assert ISO_TZ_RE.match(cd["metadata"]["last-modified"])


def test_build_component_definition_uuids_unique_per_component(
    sample_components, tmp_path: Path
) -> None:
    out = tmp_path / "cd.json"
    build_component_definition(sample_components, out, "T", "0.1.0")
    data = json.loads(out.read_text(encoding="utf-8"))
    components = data["component-definition"]["components"]

    assert len(components) == len(sample_components)
    uuids = {c["uuid"] for c in components}
    assert len(uuids) == len(components)
    for c in components:
        assert UUID_RE.match(c["uuid"])


def test_oscal_type_mapping(sample_components, tmp_path: Path) -> None:
    """Bare-metal server → hardware, VM → software, network → network."""
    out = tmp_path / "cd.json"
    build_component_definition(sample_components, out, "T", "0.1.0")
    components = json.loads(out.read_text(encoding="utf-8"))[
        "component-definition"
    ]["components"]
    by_title = {c["title"]: c for c in components}
    assert by_title["brisket"]["type"] == "hardware"
    assert by_title["dojo"]["type"] == "software"
    assert by_title["opnsense"]["type"] == "hardware"
    assert by_title["mokerlink"]["type"] == "network"


def test_component_props_include_homelab_metadata(
    sample_components, tmp_path: Path
) -> None:
    out = tmp_path / "cd.json"
    build_component_definition(sample_components, out, "T", "0.1.0")
    components = json.loads(out.read_text(encoding="utf-8"))[
        "component-definition"
    ]["components"]
    brisket = next(c for c in components if c["title"] == "brisket")
    props = {p["name"]: p["value"] for p in brisket["props"]}
    assert props["asset-id"] == "MSS-HOST-BRISKET"
    assert props["ipv4-address"] == "10.10.20.30"
    assert props["asset-tag"] == "HOMELAB-001"
    assert props["diagram-label"] == "S1"
    assert props["os-name"] == "Ubuntu"
    assert props["os-version"] == "24.04"
    assert props["hardware-model"] == "Lenovo ThinkStation"
    assert props["boundary"] == "in"
    assert props["is-virtual"] == "false"
    assert props["authenticated-scan"] == "true"


def test_component_has_no_status_field(sample_components, tmp_path: Path) -> None:
    """OSCAL component-definition components do NOT carry a status field --
    that lives in system-implementation. Verified by round-tripping through
    ``trestle.oscal.component.ComponentDefinition`` on 2026-04-09; ``status``
    raises 'extra fields not permitted'."""
    out = tmp_path / "cd.json"
    build_component_definition(sample_components, out, "T", "0.1.0")
    for c in json.loads(out.read_text(encoding="utf-8"))[
        "component-definition"
    ]["components"]:
        assert "status" not in c


def test_empty_prop_values_are_omitted(tmp_path: Path) -> None:
    """OSCAL rejects empty-string prop values. A minimal component with no
    asset_tag/diagram_label/os/hardware should still emit a valid doc."""
    minimal = InventoryComponent(
        unique_id="MSS-HOST-BARE",
        hostname="bare",
        ip_address="10.10.20.99",
        is_virtual=False,
        asset_type="Server",
        function="Minimal",
    )
    out = tmp_path / "cd.json"
    build_component_definition([minimal], out, "T", "0.1.0")
    comp = json.loads(out.read_text(encoding="utf-8"))[
        "component-definition"
    ]["components"][0]
    prop_names = {p["name"] for p in comp["props"]}
    # Optional fields must NOT be present as empty props
    assert "asset-tag" not in prop_names
    assert "diagram-label" not in prop_names
    assert "os-name" not in prop_names
    assert "os-version" not in prop_names
    assert "hardware-model" not in prop_names
    # Required props are still present
    assert "asset-id" in prop_names
    assert "ipv4-address" in prop_names
    assert "is-virtual" in prop_names
    assert "boundary" in prop_names
    assert "authenticated-scan" in prop_names
    # Every remaining prop has a non-empty value
    for p in comp["props"]:
        assert p["value"]


def test_output_path_parent_created_if_missing(
    sample_components, tmp_path: Path
) -> None:
    out = tmp_path / "nested" / "dir" / "cd.json"
    build_component_definition(sample_components, out, "T", "0.1.0")
    assert out.exists()


def test_last_modified_uses_utc_with_colon_offset(
    sample_components, tmp_path: Path
) -> None:
    """OSCAL schema requires ISO 8601 with explicit timezone offset, and
    historically tooling is stricter with the ``HH:MM`` form than ``HHMM``."""
    out = tmp_path / "cd.json"
    build_component_definition(sample_components, out, "T", "0.1.0")
    data = json.loads(out.read_text(encoding="utf-8"))
    stamp = data["component-definition"]["metadata"]["last-modified"]
    # Must end in Z or +HH:MM (with the colon)
    assert stamp.endswith("Z") or re.search(r"[+-]\d{2}:\d{2}$", stamp)
