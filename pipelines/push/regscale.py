"""Best-effort OSCAL push to RegScale CE.

Per ADR 0006 Deviation 7, RegScale CE has no long-lived API key — the
client re-authenticates per invocation via
:class:`pipelines.common.regscale.RegScaleClient`. Per a live Swagger
probe on 2026-04-09, CE also has **no generic OSCAL import endpoints**
in its API: the 13 OSCAL-prefixed paths are all export or validation
(``/api/oscal/ValidateFedRAMP``, ``/api/oscal/ValidateNIST``,
``/api/catalogues/OSCALExport/...``), none of them accept a POSTed
OSCAL artifact for import.

**Push strategy:**

1. Attempt an OSCAL validation call via
   ``POST /api/oscal/ValidateFedRAMP`` (best-effort — on failure,
   the validation is skipped and noted in the result).
2. If :data:`OSCAL_IMPORT_PATHS` has a real path for the requested
   ``oscal_type``, POST the artifact there and return
   ``status="ok"``. Today this dict is **empty** because CE exposes
   no such endpoint.
3. Otherwise, return ``status="manual-required"`` and point the
   operator at :data:`MANUAL_RUNBOOK_PATH`
   (``runbooks/regscale-manual-import.md``), which has a
   step-by-step UI-based import sequence.

When a future RegScale CE version ships generic import endpoints,
populate :data:`OSCAL_IMPORT_PATHS` with the real paths and the push
will automatically take over without code changes.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from pipelines.common.logging import get_logger
from pipelines.common.regscale import RegScaleClient


logger = get_logger(__name__)


OscalType = Literal["ssp", "poam", "component-definition", "catalog", "profile"]


# Populated only when RegScale CE exposes generic import endpoints.
# Empty today — ``push_oscal_to_regscale`` therefore returns
# ``manual-required`` for every call. When CE ships these endpoints
# in a future version, populate this dict and the push pipeline will
# switch automatically without a code change.
OSCAL_IMPORT_PATHS: dict[str, str] = {}


MANUAL_RUNBOOK_PATH: Path = Path("runbooks/regscale-manual-import.md")

VALIDATE_FEDRAMP_PATH: str = "/api/oscal/ValidateFedRAMP"


def _try_validate(
    client: RegScaleClient, payload: dict[str, Any]
) -> str:
    """Attempt the ValidateFedRAMP call. Return a human-readable result."""
    try:
        body = client.post(VALIDATE_FEDRAMP_PATH, json_body=payload)
    except Exception as exc:  # noqa: BLE001 — best-effort
        logger.warning(
            "RegScale ValidateFedRAMP call failed (%s); validation skipped", exc
        )
        return f"validation skipped: {exc}"
    logger.info("RegScale ValidateFedRAMP ok: %s", body)
    return f"validated: {body}"


def push_oscal_to_regscale(
    client: RegScaleClient,
    oscal_path: Path,
    oscal_type: OscalType,
) -> dict[str, Any]:
    """Best-effort push of an OSCAL artifact to RegScale CE.

    Args:
        client: A :class:`RegScaleClient` instance.
        oscal_path: path to the OSCAL JSON file on disk.
        oscal_type: one of ``ssp``, ``poam``, ``component-definition``,
            ``catalog``, ``profile``.

    Returns:
        A status dict. Possible shapes:

        * ``{"status": "error", "body": "...", ...}`` — file missing
          or client errored out on a non-validation call.
        * ``{"status": "manual-required", "runbook": "...",
          "validation": "..."}`` — the common case today: CE has no
          import endpoint, so the operator must use the UI runbook.
        * ``{"status": "ok", "regscale_id": ...}`` — a future CE
          release exposed the import endpoint and the push succeeded.
    """
    if not oscal_path.exists():
        return {
            "status": "error",
            "oscal_type": oscal_type,
            "body": f"{oscal_path} not found",
        }

    payload = json.loads(oscal_path.read_text(encoding="utf-8"))
    validation_result = _try_validate(client, payload)

    import_path = OSCAL_IMPORT_PATHS.get(oscal_type)
    if import_path:
        logger.info("posting %s to %s", oscal_path.name, import_path)
        body = client.post(import_path, json_body=payload)
        regscale_id = body.get("id") or body.get("uuid") or "unknown"
        return {
            "status": "ok",
            "oscal_type": oscal_type,
            "regscale_id": regscale_id,
            "validation": validation_result,
        }

    logger.info(
        "no import endpoint for oscal_type=%s -- manual import required",
        oscal_type,
    )
    return {
        "status": "manual-required",
        "oscal_type": oscal_type,
        "runbook": str(MANUAL_RUNBOOK_PATH),
        "validation": validation_result,
        "note": (
            "RegScale CE exposes no generic OSCAL import endpoint as of "
            "2026-04-09. Follow the runbook for UI-based import."
        ),
    }
