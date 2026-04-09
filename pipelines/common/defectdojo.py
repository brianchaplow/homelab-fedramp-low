"""Minimal DefectDojo API v2 client.

Scoped to the surface the FedRAMP Low ConMon pipelines need: list
products, list + create engagements, import findings via the Generic
Findings Import endpoint, list findings. Authentication is via the
DefectDojo ``Authorization: Token <api-key>`` header.

TLS verification defaults to ``False`` because the homelab DefectDojo
bundled nginx container serves http:// on port 8080 (ADR 0004). Even
when using verify=True this is a no-op for the http path; it only
matters if a future deployment terminates TLS in front of it.
"""
from __future__ import annotations

import json
import tempfile
from datetime import date
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


class DefectDojoClient:
    def __init__(
        self,
        url: str,
        api_key: str,
        verify: bool = False,
    ) -> None:
        self.url = url.rstrip("/")
        self.api_key = api_key
        self.verify = verify
        self.headers = {
            "Authorization": f"Token {api_key}",
            "Accept": "application/json",
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def list_products(self) -> list[dict[str, Any]]:
        """Return all products visible to the current API key."""
        resp = requests.get(
            f"{self.url}/api/v2/products/",
            headers=self.headers,
            verify=self.verify,
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json().get("results", [])

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def list_engagements(
        self, product_id: int | None = None
    ) -> list[dict[str, Any]]:
        params = {"product": product_id} if product_id is not None else None
        resp = requests.get(
            f"{self.url}/api/v2/engagements/",
            headers=self.headers,
            params=params,
            verify=self.verify,
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json().get("results", [])

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def create_engagement(
        self,
        product_id: int,
        name: str,
        status: str = "In Progress",
    ) -> dict[str, Any]:
        today = date.today().isoformat()
        resp = requests.post(
            f"{self.url}/api/v2/engagements/",
            headers={**self.headers, "Content-Type": "application/json"},
            json={
                "name": name,
                "product": product_id,
                "target_start": today,
                "target_end": today,
                "status": status,
                "engagement_type": "CI/CD",
            },
            verify=self.verify,
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def import_generic_findings(
        self,
        engagement_id: int,
        scan_type: str,
        findings_json: dict[str, Any],
    ) -> dict[str, Any]:
        """Import findings via the /api/v2/import-scan/ endpoint.

        Uses the Generic Findings Import format which expects
        ``{"findings": [{...}]}`` JSON uploaded as a multipart file.
        """
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as tf:
            json.dump(findings_json, tf)
            tf.flush()
            tf_path = tf.name

        try:
            with open(tf_path, "rb") as fh:
                resp = requests.post(
                    f"{self.url}/api/v2/import-scan/",
                    headers=self.headers,
                    data={
                        "engagement": engagement_id,
                        "scan_type": scan_type,
                        "active": True,
                        "verified": False,
                    },
                    files={"file": ("findings.json", fh, "application/json")},
                    verify=self.verify,
                    timeout=120,
                )
        finally:
            import os

            try:
                os.unlink(tf_path)
            except OSError:
                pass

        resp.raise_for_status()
        return resp.json()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def _findings_page(
        self, params: dict[str, Any]
    ) -> dict[str, Any]:
        resp = requests.get(
            f"{self.url}/api/v2/findings/",
            headers=self.headers,
            params=params,
            verify=self.verify,
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()

    def list_findings(
        self,
        product_id: int | None = None,
        limit: int = 1000,
        max_pages: int | None = None,
    ) -> list[dict[str, Any]]:
        """Return every finding visible to the current API key.

        The DefectDojo /api/v2/findings/ endpoint caps each page at
        1000 rows. This method auto-paginates via offset until the
        ``next`` link is null, so callers that want the full backlog
        (Task 12 POA&M builder, for example) do not have to worry about
        the cap. Pass ``max_pages`` to stop early.
        """
        all_rows: list[dict[str, Any]] = []
        offset = 0
        page = 0
        while True:
            params: dict[str, Any] = {"limit": limit, "offset": offset}
            if product_id is not None:
                params["product"] = product_id
            body = self._findings_page(params)
            results = body.get("results", [])
            all_rows.extend(results)
            page += 1
            if not body.get("next"):
                break
            if max_pages is not None and page >= max_pages:
                break
            offset += len(results) or limit
        return all_rows
