"""Build an OSCAL ``component-definition`` JSON from InventoryComponent records.

Output conforms to the NIST OSCAL ``component-definition`` schema at
version 1.1.2, which is the shape RegScale CE imports and what the
FedRAMP RFC-0024 machine-readable package mandate requires.

Scope of this module is deliberately narrow -- it takes a list of
:class:`pipelines.common.schemas.InventoryComponent`, assigns UUIDs,
maps ``asset_type`` + ``is_virtual`` to an OSCAL component type, and
flattens the homelab metadata into OSCAL ``props``. Schema validation
happens at the outer CLI layer via ``trestle validate``; this module
just writes a well-formed dict.

**OSCAL type mapping:**

* ``Network`` → ``network``
* ``Container`` or ``VM`` or ``is_virtual=True`` → ``software``
* anything else bare-metal (``Server``, ``Appliance``) → ``hardware``

These three cover every asset in the homelab overlay. The ``this-system``
type is reserved for the outer SSP authorization boundary and is not
used inside a component-definition.

Two OSCAL schema nuances verified via round-tripping through
``trestle.oscal.component.ComponentDefinition`` on 2026-04-09:

* ``status`` is **not** a field on a component inside a
  component-definition. It only exists in the system-implementation
  component schema. Emitting it causes "extra fields not permitted".
* Prop ``value`` strings must match ``^\\S(.*\\S)?$`` -- empty strings
  and whitespace-only strings are rejected. Optional inventory fields
  (``asset_tag``, ``hardware_model``, ``diagram_label``, etc.) are
  therefore **omitted** rather than emitted as empty-string props.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pipelines.common.logging import get_logger
from pipelines.common.schemas import InventoryComponent


logger = get_logger(__name__)

OSCAL_VERSION: str = "1.1.2"


def _now_iso() -> str:
    """Return the current UTC time as an OSCAL-friendly ISO 8601 string.

    OSCAL tooling is strict about the timezone offset format -- it must be
    ``Z`` or ``+HH:MM`` (with the colon). ``datetime.isoformat()`` on a
    timezone-aware datetime produces the colon form automatically.
    """
    return datetime.now(timezone.utc).isoformat()


def _oscal_type(component: InventoryComponent) -> str:
    """Map asset_type + is_virtual to an OSCAL component type string."""
    if component.asset_type == "Network":
        return "network"
    if component.asset_type in ("Container", "VM") or component.is_virtual:
        return "software"
    return "hardware"


def _component_to_oscal(component: InventoryComponent) -> dict[str, Any]:
    """Convert one InventoryComponent to an OSCAL component dict.

    Every non-empty field on the InventoryComponent round-trips into an
    OSCAL prop so the IIW renderer (Task 9) has enough data to populate
    the full FedRAMP Integrated Inventory Workbook without re-reading
    the source overlay. Props are emitted only when non-empty -- OSCAL
    rejects empty-string prop values.

    The ``title``, ``description``, and ``purpose`` top-level fields
    carry the hostname and function respectively so a Trestle-based
    reader sees the component correctly even if it ignores props.
    """
    props: list[dict[str, str]] = []

    def _maybe(name: str, value: str | None) -> None:
        if value:
            props.append({"name": name, "value": value})

    # Asset identity + topology
    _maybe("asset-id", component.unique_id)
    _maybe("ipv4-address", component.ip_address)
    _maybe("mac-address", component.mac_address)
    _maybe("dns-name", component.dns_name)
    _maybe("netbios-name", component.netbios_name)

    # Classification
    _maybe("asset-type", component.asset_type)
    _maybe("boundary", component.boundary)
    _maybe("is-virtual", str(component.is_virtual).lower())
    _maybe("is-public", str(component.is_public).lower())

    # Scan posture
    _maybe("authenticated-scan", str(component.authenticated_scan).lower())
    _maybe("in-latest-scan", str(component.in_latest_scan).lower())
    _maybe("baseline-config", component.baseline_config)

    # OS + patch level
    _maybe("os-name", component.os_name)
    _maybe("os-version", component.os_version)
    _maybe("patch-level", component.patch_level)

    # Hardware + software
    _maybe("hardware-model", component.hardware_model)
    _maybe("software-vendor", component.software_vendor)
    _maybe("software-name", component.software_name)

    # Operational metadata
    _maybe("location", component.location)
    _maybe("function", component.function)
    _maybe("diagram-label", component.diagram_label)
    _maybe("asset-tag", component.asset_tag)
    _maybe("end-of-life", component.end_of_life)
    _maybe("comments", component.comments)

    return {
        "uuid": str(uuid.uuid4()),
        "type": _oscal_type(component),
        "title": component.hostname,
        "description": component.function,
        "purpose": component.function,
        "props": props,
    }


def build_component_definition(
    components: list[InventoryComponent],
    output_path: Path,
    title: str = "Managed SOC Service",
    version: str = "0.1.0",
) -> Path:
    """Build and write an OSCAL ``component-definition`` JSON.

    Args:
        components: list of InventoryComponent records (in-boundary only).
        output_path: where to write the JSON. Parent directories are
            created if missing.
        title: component-definition metadata title.
        version: component-definition metadata version string.

    Returns:
        The ``output_path`` that was written, so the caller can chain.
    """
    cd: dict[str, Any] = {
        "component-definition": {
            "uuid": str(uuid.uuid4()),
            "metadata": {
                "title": title,
                "last-modified": _now_iso(),
                "version": version,
                "oscal-version": OSCAL_VERSION,
            },
            "components": [_component_to_oscal(c) for c in components],
        }
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(cd, indent=2), encoding="utf-8")
    logger.info(
        "wrote OSCAL component-definition with %d components to %s",
        len(components),
        output_path,
    )
    return output_path
