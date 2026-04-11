"""Wazuh Indexer (OpenSearch) client for vulnerability state reads.

Wazuh 4.8 removed the REST ``/vulnerability/{agent_id}`` endpoint. Per
ADR 0006 Deviation 5, every agent's vulnerability state is stored in the
``wazuh-states-vulnerabilities-*`` index on the Wazuh Indexer, keyed by
``agent.id`` / ``agent.name``. Live probe of v4.14.4 on 2026-04-09
confirmed 12,949 documents in the ``wazuh.manager`` single-node cluster,
with the schema::

    _source.agent.name
    _source.agent.id
    _source.vulnerability.id          (CVE identifier)
    _source.vulnerability.severity    (Critical/High/Medium/Low/Info)
    _source.vulnerability.score.base  (CVSS base score)
    _source.vulnerability.detected_at (ISO 8601)
    _source.vulnerability.description
    _source.vulnerability.reference   (URL string -- downstream may split)
    _source.package.name
    _source.package.version

This client provides a thin, mockable interface over that index: a
single ``search_vulnerabilities()`` method that accepts an ``agent_name``
and returns every hit as a raw OpenSearch document. Paging is handled
internally via ``search_after`` so callers do not need to worry about
the 10,000-row scroll ceiling.

Transport details mirror :class:`pipelines.common.wazuh.WazuhClient`:
basic auth against the indexer (user defaults to ``admin``, password
from ``WAZUH_INDEXER_PASSWORD``), TLS verification off by default for
the self-signed lab cert, and retry-with-backoff on transient errors.
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


VULN_INDEX_PATTERN: str = "wazuh-states-vulnerabilities-*"


class WazuhIndexerClient:
    """Thin OpenSearch client for Wazuh vulnerability state reads.

    Args:
        url: Wazuh Indexer base URL, typically ``https://10.10.20.30:9200``.
        user: OpenSearch user (``admin`` by convention).
        password: OpenSearch password.
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

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def _search(self, body: dict[str, Any]) -> dict[str, Any]:
        """POST a search DSL body to the vuln index pattern."""
        url = f"{self.url}/{VULN_INDEX_PATTERN}/_search"
        resp = requests.post(
            url,
            auth=(self.user, self.password),
            json=body,
            verify=self.verify,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def search_vulnerabilities(
        self,
        agent_name: str,
        page_size: int = 500,
    ) -> list[dict[str, Any]]:
        """Return every vulnerability document for a given agent name.

        The query uses a ``term`` filter on ``agent.name`` and pages via
        ``search_after`` on a deterministic sort
        (``vulnerability.detected_at`` then ``_id`` as a stable tiebreaker).
        Live probe on 2026-04-09 showed ``vulnerability.id`` is already a
        ``keyword`` type but is not unique across re-detects of the same
        package -- ``_id`` is the only reliably unique sort key, so we use
        it as the tiebreaker. Empty page signals the end of results.

        Args:
            agent_name: Wazuh agent name (e.g. ``"dojo"``).
            page_size: Number of hits per request. Defaults to 500 --
                well under the 10k scroll limit and large enough that
                most agents are one or two requests.

        Returns:
            A flat list of OpenSearch hits in document form (each hit is
            the full JSON object including ``_index``, ``_id``, and
            ``_source``). Downstream mappers in Task 10 read
            ``hit['_source'][...]`` to build normalized Findings.
        """
        all_hits: list[dict[str, Any]] = []
        search_after: list[Any] | None = None

        sort_clause = [
            {"vulnerability.detected_at": "asc"},
            {"_id": "asc"},
        ]

        while True:
            body: dict[str, Any] = {
                "size": page_size,
                "query": {"term": {"agent.name": agent_name}},
                "sort": sort_clause,
            }
            if search_after is not None:
                body["search_after"] = search_after

            resp = self._search(body)
            hits = resp.get("hits", {}).get("hits", [])
            if not hits:
                break

            all_hits.extend(hits)
            if len(hits) < page_size:
                break

            last_sort = hits[-1].get("sort")
            if not last_sort:
                # No sort value -- we cannot page further safely
                logger.warning(
                    "search_after paging halted: last hit has no sort key"
                )
                break
            search_after = last_sort

        logger.info(
            "Wazuh indexer: %d vuln hits for agent %s", len(all_hits), agent_name
        )
        return all_hits
