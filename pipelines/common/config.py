"""Configuration loader for FedRAMP pipelines.

This module is the single source of truth for every credential and endpoint
the pipelines talk to. It follows a *hybrid* env-var strategy per ADR 0006
Deviation 4:

* Architectural constants (Wazuh API URL, Wazuh API user, Wazuh indexer URL,
  Wazuh indexer user) live in code as ``*_DEFAULT`` constants. They are
  stable across the homelab and do not need to sit in ``.env``. A fork
  targeting a different Wazuh host can still override each of them via an
  env var of the same name (e.g. ``WAZUH_API_URL``) without touching code.
* Secrets (passwords, API keys, DefectDojo/RegScale URLs which are
  operator-specific) are **required** from the environment. If any is
  missing, ``load_config()`` raises with every missing name in the error
  message so the operator sees the whole gap at once.

HTTPS enforcement is scoped to Wazuh endpoints only (ADR 0006 Deviation 3).
DefectDojo and RegScale CE run plain HTTP in the lab (ADRs 0004 and 0003
respectively) and a validator that rejected ``http://`` would fail every
pipeline invocation at startup.

No ``REGSCALE_API_KEY`` exists anywhere — RegScale CE has no long-lived
bearer token. The client re-authenticates per invocation via JWT
(ADR 0006 Deviation 7).
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, field_validator


# ---------------------------------------------------------------------------
# Architectural constants (ADR 0006 Deviation 4)
#
# These are the stable values for the homelab SOC. Each is overrideable via an
# env var of the same name so the pipelines can target a different Wazuh
# deployment without a code change.
# ---------------------------------------------------------------------------

WAZUH_API_URL_DEFAULT: str = "https://10.10.20.30:55000"
WAZUH_API_USER_DEFAULT: str = "wazuh-wui"
WAZUH_INDEXER_URL_DEFAULT: str = "https://10.10.20.30:9200"
WAZUH_INDEXER_USER_DEFAULT: str = "admin"


# ---------------------------------------------------------------------------
# Required env vars — secrets and operator-specific URLs only
# ---------------------------------------------------------------------------

REQUIRED_ENV_VARS: tuple[str, ...] = (
    "WAZUH_API_PASSWORD",
    "WAZUH_INDEXER_PASSWORD",
    "DEFECTDOJO_URL",
    "DEFECTDOJO_API_KEY",
    "REGSCALE_URL",
    "REGSCALE_USERNAME",
    "REGSCALE_PASSWORD",
)


class Config(BaseModel):
    """Frozen pipeline configuration. All values come from env vars or defaults.

    The HTTPS validator is intentionally asymmetric — it applies to
    ``wazuh_api_url`` and ``wazuh_indexer_url`` only. DefectDojo and RegScale
    URLs accept ``http://`` because that is what the lab appliances actually
    serve (see ADRs 0003, 0004, and 0006 Deviation 3).
    """

    model_config = ConfigDict(frozen=True)

    # Wazuh API (REST) ------------------------------------------------------
    wazuh_api_url: str
    wazuh_api_user: str
    wazuh_api_password: str

    # Wazuh Indexer (OpenSearch) -------------------------------------------
    wazuh_indexer_url: str
    wazuh_indexer_user: str
    wazuh_indexer_password: str

    # DefectDojo (HTTP, Token auth) ----------------------------------------
    defectdojo_url: str
    defectdojo_api_key: str

    # RegScale CE (HTTP, JWT re-auth per invocation) -----------------------
    regscale_url: str
    regscale_username: str
    regscale_password: str

    @field_validator("wazuh_api_url", "wazuh_indexer_url")
    @classmethod
    def must_start_with_https(cls, v: str) -> str:
        if not v.startswith("https://"):
            raise ValueError(f"Wazuh endpoints must use https://: {v}")
        return v


def load_config(env_file: Path | None = None) -> Config:
    """Load configuration from environment variables.

    If ``env_file`` is provided and exists, it is pre-loaded via python-dotenv
    before env vars are read. In the homelab, ``pipelines.sh`` sources
    ``/c/Projects/.env`` before invoking any pipeline, so callers do not
    normally need to pass ``env_file``. It exists for ad-hoc use from
    notebooks or one-off scripts.

    Architectural defaults (Wazuh URLs/users) fall back to the constants
    defined at module scope if the corresponding env var is unset. Secrets
    and operator-specific URLs are required — a missing value raises with
    every missing name in the error message.

    Raises:
        ValueError: if any required env var is missing, or if a Wazuh URL
            does not start with ``https://``.
    """
    if env_file is not None and env_file.exists():
        load_dotenv(env_file)

    missing = [v for v in REQUIRED_ENV_VARS if not os.environ.get(v)]
    if missing:
        raise ValueError(
            "missing required env vars: "
            + ", ".join(missing)
            + " (set them in /c/Projects/.env or pass env_file=)"
        )

    return Config(
        wazuh_api_url=os.environ.get("WAZUH_API_URL", WAZUH_API_URL_DEFAULT),
        wazuh_api_user=os.environ.get("WAZUH_API_USER", WAZUH_API_USER_DEFAULT),
        wazuh_api_password=os.environ["WAZUH_API_PASSWORD"],
        wazuh_indexer_url=os.environ.get(
            "WAZUH_INDEXER_URL", WAZUH_INDEXER_URL_DEFAULT
        ),
        wazuh_indexer_user=os.environ.get(
            "WAZUH_INDEXER_USER", WAZUH_INDEXER_USER_DEFAULT
        ),
        wazuh_indexer_password=os.environ["WAZUH_INDEXER_PASSWORD"],
        defectdojo_url=os.environ["DEFECTDOJO_URL"],
        defectdojo_api_key=os.environ["DEFECTDOJO_API_KEY"],
        regscale_url=os.environ["REGSCALE_URL"],
        regscale_username=os.environ["REGSCALE_USERNAME"],
        regscale_password=os.environ["REGSCALE_PASSWORD"],
    )
