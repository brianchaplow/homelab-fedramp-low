"""Wazuh API REST client with JWT auth and retry-with-backoff.

This client covers the Wazuh REST surface that the FedRAMP Low pipelines
actually use — agent listing and syscollector (OS / hardware / packages).
It does **not** expose a ``get_vulnerabilities()`` method: Wazuh 4.8
removed the ``/vulnerability/{agent_id}`` REST endpoint, and a live probe
against v4.14.4 returned HTTP 404 for every variant. Vulnerability state
now lives exclusively in the ``wazuh-states-vulnerabilities-*`` index on
the Wazuh Indexer and is reached via
:class:`pipelines.common.wazuh_indexer.WazuhIndexerClient`. See ADR 0006
Deviation 5 for the full rationale and live-probe evidence.

Transport details:

* TLS verification is off by default — the Wazuh manager serves a
  self-signed cert that is trusted at the lab posture level, documented in
  ``runbooks/cert-trust.md``. ``urllib3`` warnings are suppressed once at
  module import to avoid spamming the pipeline log.
* Retries are tenacity-backed, exponential backoff, up to 3 attempts.
* JWT is cached and re-issued on 401. One re-auth attempt is allowed per
  request before raising so a stale token does not cause silent retry
  loops.
"""
from __future__ import annotations

from typing import Any

import requests
import urllib3
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from pipelines.common.logging import get_logger


# Self-signed certs in lab — suppress once at import time.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = get_logger(__name__)


class WazuhClient:
    """Thin REST client for the Wazuh manager API.

    Authenticates lazily on first request, caches the JWT, re-authenticates
    on 401. All HTTP calls retry with exponential backoff up to 3 attempts
    on transient ``requests.RequestException``.

    Args:
        url: Wazuh API base URL, typically ``https://10.10.20.30:55000``.
        user: API user (``wazuh-wui`` in the homelab by convention).
        password: API password.
        verify: TLS verification. Defaults to ``False`` for the lab
            self-signed cert posture.
    """

    def __init__(
        self,
        url: str,
        user: str,
        password: str,
        verify: bool = False,
    ) -> None:
        self.url = url.rstrip("/")
        self.user = user
        self.password = password
        self.verify = verify
        self._token: str | None = None

    # ---- authentication --------------------------------------------------

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def authenticate(self) -> str:
        """POST ``/security/user/authenticate`` and cache the returned JWT."""
        resp = requests.post(
            f"{self.url}/security/user/authenticate",
            auth=(self.user, self.password),
            verify=self.verify,
            timeout=10,
        )
        resp.raise_for_status()
        token = resp.json().get("data", {}).get("token")
        if not token:
            raise ValueError("Wazuh auth response missing token")
        self._token = token
        logger.info("Wazuh authentication successful")
        return token

    def _headers(self) -> dict[str, str]:
        if self._token is None:
            self.authenticate()
        return {"Authorization": f"Bearer {self._token}"}

    # ---- core GET with 401 re-auth --------------------------------------

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def get(
        self, path: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Authenticated GET. Re-auths exactly once on 401."""
        url = f"{self.url}{path}"
        for attempt in (1, 2):
            resp = requests.get(
                url,
                headers=self._headers(),
                params=params,
                verify=self.verify,
                timeout=30,
            )
            if resp.status_code == 401 and attempt == 1:
                logger.info("401 from Wazuh, re-authenticating")
                self._token = None
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError("Wazuh API auth loop exhausted")

    # ---- agents + syscollector -----------------------------------------

    def list_agents(self, status: str | None = None) -> list[dict[str, Any]]:
        """Return agents, optionally filtered by ``status`` (e.g. ``"active"``)."""
        params = {"status": status} if status else None
        data = self.get("/agents", params=params)
        return data.get("data", {}).get("affected_items", [])

    def get_syscollector_os(self, agent_id: str) -> dict[str, Any]:
        """Return the OS record for an agent (or ``{}`` if empty)."""
        data = self.get(f"/syscollector/{agent_id}/os")
        items = data.get("data", {}).get("affected_items", [])
        return items[0] if items else {}

    def get_syscollector_hardware(self, agent_id: str) -> dict[str, Any]:
        """Return the hardware record for an agent (or ``{}`` if empty)."""
        data = self.get(f"/syscollector/{agent_id}/hardware")
        items = data.get("data", {}).get("affected_items", [])
        return items[0] if items else {}

    def get_syscollector_packages(
        self, agent_id: str, limit: int = 1000
    ) -> list[dict[str, Any]]:
        """Return installed packages for an agent, capped at ``limit`` rows."""
        data = self.get(
            f"/syscollector/{agent_id}/packages", params={"limit": limit}
        )
        return data.get("data", {}).get("affected_items", [])
