"""RegScale CE JWT client.

Per ADR 0006 Deviation 7, RegScale CE has no long-lived API key. The
only supported authentication flow is ``POST /api/authentication/login``
with a JSON body of ``{"username": "...", "password": "..."}`` — the
response carries a 24-hour JWT in the ``auth_token`` field. That JWT
is used as a ``Authorization: Bearer <token>`` header on subsequent
requests. This client caches the token, re-authenticates automatically
on a 401 response, and exposes a minimal ``get`` / ``post`` pair that
downstream pipeline code can build on.

The field name is ``username`` (lowercase), not ``userName`` — verified
against ``tests/smoke/check_regscale.sh`` which is the known-working
reference implementation.

TLS verification defaults to ``False`` because RegScale CE serves
plain ``http://`` on port 80 in the lab (ADR 0003). The verify flag
is kept on the client so a future CE deployment can flip it on.
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


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = get_logger(__name__)


class RegScaleClient:
    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        verify: bool = False,
    ) -> None:
        self.url = url.rstrip("/")
        self.username = username
        self.password = password
        self.verify = verify
        self._token: str | None = None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def authenticate(self) -> str:
        """Return a cached JWT, logging in if this is the first call."""
        if self._token is not None:
            return self._token

        resp = requests.post(
            f"{self.url}/api/authentication/login",
            json={"username": self.username, "password": self.password},
            verify=self.verify,
            timeout=15,
        )
        resp.raise_for_status()
        body = resp.json()
        token = body.get("auth_token")
        if not token:
            raise ValueError(
                "RegScale login response missing 'auth_token' field"
            )
        self._token = token
        logger.info("RegScale authentication successful")
        return token

    def _headers(self) -> dict[str, str]:
        token = self.authenticate()
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

    def get(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """Authenticated GET. Re-auths exactly once on 401."""
        url = f"{self.url}{path}"
        for attempt in (1, 2):
            resp = requests.get(
                url,
                headers=self._headers(),
                verify=self.verify,
                timeout=30,
                **kwargs,
            )
            if resp.status_code == 401 and attempt == 1:
                logger.info("RegScale 401 -> re-authenticating")
                self._token = None
                continue
            resp.raise_for_status()
            return resp.json() if resp.content else {}
        raise RuntimeError("RegScale auth loop exhausted")

    def post(
        self,
        path: str,
        json_body: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Authenticated POST. Re-auths exactly once on 401."""
        url = f"{self.url}{path}"
        for attempt in (1, 2):
            headers = {**self._headers(), "Content-Type": "application/json"}
            resp = requests.post(
                url,
                headers=headers,
                json=json_body,
                verify=self.verify,
                timeout=60,
                **kwargs,
            )
            if resp.status_code == 401 and attempt == 1:
                logger.info("RegScale 401 -> re-authenticating")
                self._token = None
                continue
            resp.raise_for_status()
            return resp.json() if resp.content else {}
        raise RuntimeError("RegScale auth loop exhausted")

    def seeding_status(self) -> dict[str, Any]:
        """Probe ``/api/SeedingStatus`` — the canonical smoke-test endpoint."""
        return self.get("/api/SeedingStatus")
