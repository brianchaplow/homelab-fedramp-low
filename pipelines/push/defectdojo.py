"""Push normalized Findings to DefectDojo via Generic Findings Import.

Groups findings by product via a ``host_to_product`` map, auto-creates
the named engagement in each product if it does not yet exist, and
imports a single scan per product. Findings whose host is not in the
map are counted as ``skipped`` so the caller can log the gap.

The DefectDojo Generic Findings Import format is documented at
https://documentation.defectdojo.com/integrations/parsers/file/generic/.
Every Finding field that has a natural DefectDojo counterpart is
carried across; optional fields are omitted when empty so the import
payload stays clean.

Product names use ASCII hyphens (e.g. ``"MSS Core - brisket"``) per
ADR 0006 amendment 2026-04-09 -- the Plan 1 seed script created them
with ``-``, not em dashes.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any

from pipelines.common.defectdojo import DefectDojoClient
from pipelines.common.logging import get_logger
from pipelines.common.schemas import Finding


logger = get_logger(__name__)


def findings_to_generic_format(findings: list[Finding]) -> dict[str, Any]:
    """Convert a list of Findings to DefectDojo Generic Findings Import JSON.

    Note on the host field: DefectDojo's Generic Findings Import does
    NOT accept a top-level ``host`` key. Probing the live 2.57.0 API
    on 2026-04-09 returned
    ``"Not allowed fields are present: ['host']"``. The correct way
    to carry the affected asset is the ``endpoints`` list, which the
    parser treats as URI strings -- we pass a single-element list of
    the hostname.
    """
    out_findings: list[dict[str, Any]] = []
    for f in findings:
        item: dict[str, Any] = {
            "title": f.title,
            "description": f.description,
            "severity": f.severity.value,
            "active": True,
            "verified": False,
            "static_finding": False,
            "dynamic_finding": True,
            "unique_id_from_tool": f.finding_id,
            "date": f.discovered_date.date().isoformat(),
            "endpoints": [f.affected_host],
        }
        if f.cve:
            item["cve"] = f.cve
        if f.cvss_score is not None:
            item["cvssv3_score"] = f.cvss_score
        if f.affected_package:
            item["component_name"] = f.affected_package
        if f.references:
            item["references"] = "\n".join(f.references)
        if f.related_controls:
            item["tags"] = [f"control:{c.lower()}" for c in f.related_controls]
        out_findings.append(item)

    return {"findings": out_findings}


def _engagement_id_for_product(
    client: DefectDojoClient,
    product_id: int,
    engagement_name: str,
    existing_engagements_by_product: dict[int, list[dict[str, Any]]],
) -> int:
    """Return engagement id for the (product, name) pair, creating it if missing."""
    for eng in existing_engagements_by_product.get(product_id, []):
        if eng.get("name") == engagement_name:
            return int(eng["id"])

    created = client.create_engagement(product_id=product_id, name=engagement_name)
    logger.info(
        "created engagement '%s' in product id=%d -> engagement id=%s",
        engagement_name,
        product_id,
        created.get("id"),
    )
    return int(created["id"])


def push_findings_to_defectdojo(
    client: DefectDojoClient,
    findings: list[Finding],
    host_to_product: dict[str, str],
    engagement_name: str,
) -> dict[str, int]:
    """Group findings by product and import one scan per product.

    Args:
        client: DefectDojo client.
        findings: list of normalized Finding records.
        host_to_product: ``{hostname: product_name}`` map (ASCII hyphens).
        engagement_name: engagement to target in each product. Created
            if it does not exist.

    Returns:
        ``{"imported": int, "skipped": int}`` counts.

    Raises:
        ValueError: if any value in ``host_to_product`` names a product
            that is not present in DefectDojo. This is a fail-fast
            safety check -- mistyped product names are the most common
            cause of silent data loss in this pipeline.
    """
    products_by_name: dict[str, int] = {
        p["name"]: int(p["id"]) for p in client.list_products()
    }

    # Validate the map: every value must exist as a product in DefectDojo.
    missing_products = {
        product_name
        for product_name in set(host_to_product.values())
        if product_name not in products_by_name
    }
    if missing_products:
        raise ValueError(
            "host_to_product references unknown DefectDojo products: "
            + ", ".join(sorted(missing_products))
        )

    # Index existing engagements by product id so we can skip re-fetch.
    engagements_by_product: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for eng in client.list_engagements():
        engagements_by_product[int(eng["product"])].append(eng)

    # Group findings by product name.
    findings_by_product: dict[str, list[Finding]] = defaultdict(list)
    skipped = 0
    for f in findings:
        product_name = host_to_product.get(f.affected_host)
        if not product_name:
            skipped += 1
            continue
        findings_by_product[product_name].append(f)

    imported = 0
    for product_name, group in findings_by_product.items():
        product_id = products_by_name[product_name]
        engagement_id = _engagement_id_for_product(
            client,
            product_id,
            engagement_name,
            engagements_by_product,
        )
        payload = findings_to_generic_format(group)
        logger.info(
            "importing %d findings for product '%s' -> engagement id=%d",
            len(group),
            product_name,
            engagement_id,
        )
        client.import_generic_findings(
            engagement_id=engagement_id,
            scan_type="Generic Findings Import",
            findings_json=payload,
        )
        imported += len(group)

    logger.info("DefectDojo push complete: imported=%d skipped=%d", imported, skipped)
    return {"imported": imported, "skipped": skipped}
