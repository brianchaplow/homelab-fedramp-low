"""Tests for pipelines.common.wazuh_indexer -- OpenSearch vuln client.

Per ADR 0006 Deviation 5, Wazuh 4.8 removed the REST /vulnerability
endpoint. Vulnerability state now lives in the
``wazuh-states-vulnerabilities-*`` index on the Wazuh Indexer
(OpenSearch) and must be reached via OpenSearch DSL with basic auth.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from pipelines.common.wazuh_indexer import (
    VULN_INDEX_PATTERN,
    WazuhIndexerClient,
)


def _hit(
    agent_name: str = "dojo",
    agent_id: str = "016",
    cve: str = "CVE-2025-1376",
    severity: str = "Low",
    base: float = 2.5,
    pkg_name: str = "libelf1t64",
) -> dict:
    return {
        "_index": "wazuh-states-vulnerabilities-wazuh.manager",
        "_id": f"{agent_id}_{cve}_{pkg_name}",
        "_source": {
            "agent": {"id": agent_id, "name": agent_name},
            "package": {"name": pkg_name, "version": "1.0"},
            "vulnerability": {
                "id": cve,
                "severity": severity,
                "score": {"base": base, "version": "3.1"},
                "detected_at": "2026-04-09T16:53:18.428Z",
                "description": "A vuln",
                "reference": "https://example/cve",
            },
        },
        "sort": [1_712_685_198_428, cve],
    }


@pytest.fixture
def mock_ok_factory():
    def _make(json_data: dict, status: int = 200) -> MagicMock:
        m = MagicMock()
        m.status_code = status
        m.json.return_value = json_data
        m.raise_for_status.return_value = None
        return m

    return _make


@patch("pipelines.common.wazuh_indexer.requests.post")
def test_search_vulnerabilities_returns_hits_for_agent(
    mock_post, mock_ok_factory
):
    mock_post.return_value = mock_ok_factory(
        {"hits": {"hits": [_hit(), _hit(cve="CVE-2025-0002", pkg_name="nginx")]}}
    )
    client = WazuhIndexerClient(
        url="https://10.10.20.30:9200",
        user="admin",
        password="p",
        verify=False,
    )
    hits = client.search_vulnerabilities(agent_name="dojo")

    assert len(hits) == 2
    assert hits[0]["_source"]["vulnerability"]["id"] == "CVE-2025-1376"
    assert hits[1]["_source"]["package"]["name"] == "nginx"

    # Verify the _search URL targets the correct index pattern
    call_url = mock_post.call_args.args[0]
    assert VULN_INDEX_PATTERN in call_url
    assert "_search" in call_url

    # Verify the DSL body filters on agent.name
    body = mock_post.call_args.kwargs["json"]
    assert body["query"]["term"]["agent.name"] == "dojo"
    assert body["sort"]  # sort required for search_after paging


@patch("pipelines.common.wazuh_indexer.requests.post")
def test_search_vulnerabilities_pages_via_search_after(
    mock_post, mock_ok_factory
):
    """When the first page is full, client sends a second request with
    the last hit's ``sort`` as ``search_after``."""
    full_page = {
        "hits": {"hits": [_hit(cve=f"CVE-2025-{i:04d}") for i in range(2)]}
    }
    empty_page = {"hits": {"hits": []}}
    mock_post.side_effect = [
        mock_ok_factory(full_page),
        mock_ok_factory(empty_page),
    ]

    client = WazuhIndexerClient(
        url="https://10.10.20.30:9200", user="admin", password="p"
    )
    hits = client.search_vulnerabilities(agent_name="dojo", page_size=2)

    assert len(hits) == 2
    assert mock_post.call_count == 2
    # Second call must carry search_after equal to the previous last hit's sort
    second_body = mock_post.call_args_list[1].kwargs["json"]
    assert second_body["search_after"] == full_page["hits"]["hits"][-1]["sort"]


@patch("pipelines.common.wazuh_indexer.requests.post")
def test_search_vulnerabilities_uses_basic_auth_and_verify_false(
    mock_post, mock_ok_factory
):
    mock_post.return_value = mock_ok_factory({"hits": {"hits": []}})
    client = WazuhIndexerClient(
        url="https://10.10.20.30:9200",
        user="admin",
        password="secret",
        verify=False,
    )
    client.search_vulnerabilities(agent_name="dojo")

    kwargs = mock_post.call_args.kwargs
    assert kwargs["auth"] == ("admin", "secret")
    assert kwargs["verify"] is False


@patch("pipelines.common.wazuh_indexer.requests.post")
def test_search_vulnerabilities_raises_on_http_error(
    mock_post, mock_ok_factory
):
    bad = mock_ok_factory({}, status=500)
    bad.raise_for_status.side_effect = Exception("500 Server Error")
    mock_post.return_value = bad

    client = WazuhIndexerClient(
        url="https://10.10.20.30:9200", user="admin", password="p"
    )
    with pytest.raises(Exception, match="500"):
        client.search_vulnerabilities(agent_name="dojo")


def test_index_pattern_constant_matches_live_probe() -> None:
    """ADR 0006 Deviation 5 documents the live index pattern."""
    assert VULN_INDEX_PATTERN == "wazuh-states-vulnerabilities-*"
