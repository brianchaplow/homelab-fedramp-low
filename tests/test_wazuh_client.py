"""Tests for pipelines.common.wazuh -- Wazuh API REST client.

Per ADR 0006 Deviation 5, this client intentionally does NOT expose
``get_vulnerabilities()``. The /vulnerability/{agent_id} endpoint was
removed in Wazuh 4.8; vulnerability state now lives in the OpenSearch
indexer and is reached via :mod:`pipelines.common.wazuh_indexer` (Task 6b).
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from pipelines.common.wazuh import WazuhClient


@pytest.fixture
def mock_response_factory():
    def _make(json_data: dict, status: int = 200) -> MagicMock:
        m = MagicMock()
        m.status_code = status
        m.json.return_value = json_data
        m.raise_for_status.return_value = None
        return m

    return _make


@patch("pipelines.common.wazuh.requests.post")
@patch("pipelines.common.wazuh.requests.get")
def test_authenticate_then_list_agents(mock_get, mock_post, mock_response_factory):
    """First call authenticates, subsequent calls hit /agents with the JWT.

    Uses the current agent IDs 016 (dojo) and 017 (regscale) per ADR 0006
    Deviation 6.
    """
    mock_post.return_value = mock_response_factory(
        {"data": {"token": "test-jwt-token"}}
    )
    mock_get.return_value = mock_response_factory(
        {
            "data": {
                "affected_items": [
                    {"id": "016", "name": "dojo", "ip": "10.10.30.27", "status": "active"},
                    {"id": "017", "name": "regscale", "ip": "10.10.30.28", "status": "active"},
                ]
            }
        }
    )

    client = WazuhClient(
        url="https://10.10.20.30:55000", user="u", password="p", verify=False
    )
    agents = client.list_agents(status="active")

    assert len(agents) == 2
    assert agents[0]["id"] == "016"
    assert agents[1]["name"] == "regscale"
    mock_post.assert_called_once()
    mock_get.assert_called_once()


@patch("pipelines.common.wazuh.requests.post")
def test_authenticate_failure_raises(mock_post, mock_response_factory):
    """Authentication failure surfaces as an exception to the caller."""
    failed = mock_response_factory({}, status=401)
    failed.raise_for_status.side_effect = Exception("401 Unauthorized")
    mock_post.return_value = failed

    client = WazuhClient(
        url="https://10.10.20.30:55000", user="u", password="bad", verify=False
    )
    with pytest.raises(Exception, match="401"):
        client.authenticate()


@patch("pipelines.common.wazuh.requests.post")
def test_authenticate_missing_token_raises(mock_post, mock_response_factory):
    """If Wazuh returns a 200 without a token, fail loudly."""
    mock_post.return_value = mock_response_factory({"data": {}})
    client = WazuhClient(url="https://10.10.20.30:55000", user="u", password="p")
    with pytest.raises(ValueError, match="token"):
        client.authenticate()


@patch("pipelines.common.wazuh.requests.post")
@patch("pipelines.common.wazuh.requests.get")
def test_get_syscollector_os_returns_first_item(
    mock_get, mock_post, mock_response_factory
):
    mock_post.return_value = mock_response_factory({"data": {"token": "jwt"}})
    mock_get.return_value = mock_response_factory(
        {
            "data": {
                "affected_items": [
                    {"os": {"name": "Ubuntu", "version": "24.04"}},
                ]
            }
        }
    )
    client = WazuhClient(url="https://w:55000", user="u", password="p")
    info = client.get_syscollector_os("016")
    assert info["os"]["name"] == "Ubuntu"


@patch("pipelines.common.wazuh.requests.post")
@patch("pipelines.common.wazuh.requests.get")
def test_get_syscollector_os_empty_returns_empty_dict(
    mock_get, mock_post, mock_response_factory
):
    mock_post.return_value = mock_response_factory({"data": {"token": "jwt"}})
    mock_get.return_value = mock_response_factory({"data": {"affected_items": []}})
    client = WazuhClient(url="https://w:55000", user="u", password="p")
    assert client.get_syscollector_os("999") == {}


@patch("pipelines.common.wazuh.requests.post")
@patch("pipelines.common.wazuh.requests.get")
def test_get_syscollector_packages_returns_list(
    mock_get, mock_post, mock_response_factory
):
    mock_post.return_value = mock_response_factory({"data": {"token": "jwt"}})
    mock_get.return_value = mock_response_factory(
        {
            "data": {
                "affected_items": [
                    {"name": "nginx", "version": "1.24.0"},
                    {"name": "openssl", "version": "3.0.13"},
                ]
            }
        }
    )
    client = WazuhClient(url="https://w:55000", user="u", password="p")
    pkgs = client.get_syscollector_packages("016")
    assert len(pkgs) == 2
    assert pkgs[0]["name"] == "nginx"


def test_client_does_not_expose_get_vulnerabilities() -> None:
    """ADR 0006 Deviation 5: no REST vuln endpoint on Wazuh 4.8+."""
    assert not hasattr(WazuhClient, "get_vulnerabilities")
