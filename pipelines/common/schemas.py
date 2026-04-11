"""Pydantic models for normalized findings and inventory records.

These are the lingua franca of the FedRAMP Low pipelines. Every ingest
source normalizes its raw input into one of these shapes, and every
downstream stage (OSCAL builder, IIW renderer, POA&M builder, DefectDojo
push) consumes them. Keeping the shapes small and frozen means the cross-
stage contract is explicit and the pipelines are trivially composable.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Severity(str, Enum):
    """FedRAMP-aligned severity buckets. The enum values match DefectDojo
    and IIW/POA&M template conventions exactly so downstream renderers can
    serialize without translation."""

    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"


class FindingState(str, Enum):
    """POA&M lifecycle states. ``OPEN`` / ``VERIFIED`` / ``IN_PROGRESS`` map
    to active FedRAMP POA&M items; ``COMPLETED`` / ``CLOSED`` move to the
    closed sheet; ``FALSE_POSITIVE`` and ``DEVIATED`` carry their own
    FedRAMP-specific handling (deviation requests, vendor dependencies)."""

    OPEN = "Open"
    VERIFIED = "Verified"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CLOSED = "Closed"
    FALSE_POSITIVE = "False Positive"
    DEVIATED = "Deviated"


class Finding(BaseModel):
    """A normalized vulnerability or scan finding.

    The ``finding_id`` field must be stable across re-scans of the same
    host so that DefectDojo deduplicates correctly and so that POA&M
    numbering survives across ConMon cycles. A typical shape is
    ``<host>:<cve>:<package>`` for Wazuh vuln hits or the upstream
    scanner's own stable id.
    """

    model_config = ConfigDict(frozen=True)

    finding_id: str = Field(
        description="Stable identifier across re-scans (host:cve:package or scan tool's stable id)"
    )
    title: str
    description: str
    severity: Severity
    state: FindingState = FindingState.OPEN
    cve: str | None = None
    cvss_score: float | None = None
    affected_host: str = Field(description="Hostname or IP of the asset with the finding")
    affected_component: str | None = None
    affected_package: str | None = None
    discovered_date: datetime
    last_seen_date: datetime
    source_tool: Literal["wazuh-vuln", "nuclei", "wazuh-sca", "manual"]
    references: list[str] = Field(default_factory=list)
    related_controls: list[str] = Field(
        default_factory=list,
        description="NIST 800-53 control IDs (e.g., ['SI-2', 'RA-5'])",
    )


class InventoryComponent(BaseModel):
    """A normalized inventory component -- one row of the FedRAMP Integrated
    Inventory Workbook.

    Field names match the IIW column headers closely enough that the
    renderer is a straight mapping. Defaults bias toward the common case
    for the homelab (on-prem rack in Virginia, authenticated scanning, in
    boundary) so overlay files only need to specify exceptions.
    """

    model_config = ConfigDict(frozen=True)

    unique_id: str
    hostname: str
    ip_address: str
    mac_address: str | None = None
    is_virtual: bool
    is_public: bool = False
    dns_name: str | None = None
    netbios_name: str | None = None
    authenticated_scan: bool = True
    baseline_config: str | None = None
    os_name: str | None = None
    os_version: str | None = None
    location: str = "On-prem homelab rack, Virginia"
    asset_type: Literal["Server", "Network", "Appliance", "VM", "Container"]
    hardware_model: str | None = None
    in_latest_scan: bool = True
    software_vendor: str | None = None
    software_name: str | None = None
    patch_level: str | None = None
    diagram_label: str | None = None
    function: str
    asset_tag: str | None = None
    end_of_life: str | None = None
    boundary: Literal["in", "out"] = "in"
    comments: str = ""
