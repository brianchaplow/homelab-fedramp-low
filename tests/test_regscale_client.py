"""Tests for pipelines.common.regscale -- RegScale CE JWT client.

Per ADR 0006 Deviation 7, RegScale CE has no long-lived API key. Auth
is via POST /api/authentication/login with username/password, returning
a 24-hour JWT in the ``auth_token`` field. This module caches the JWT
and re-auths on 401.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from pipelines.common.regscale import RegScaleClient


@pytest.fixture
def mock_resp_factory():
    def _make(json_data: dict, status: int = 200) -> MagicMock:
        m = MagicMock()
        m.status_code = status
        m.json.return_value = json_data
        m.raise_for_status.return_value = None
        return m

    return _make


@patch("pipelines.common.regscale.requests.post")
def test_authenticate_posts_username_password_and_caches_token(
    mock_post, mock_resp_factory
):
    mock_post.return_value = mock_resp_factory(
        {"auth_token": "jwt-ABC", "id": 1}
    )
    c = RegScaleClient(
        url="http://10.10.30.28", username="admin", password="pw", verify=False
    )
    token = c.authenticate()
    assert token == "jwt-ABC"
    assert c._token == "jwt-ABC"
    # Next call should NOT re-auth -- token is cached
    token2 = c.authenticate()
    assert token2 == "jwt-ABC"
    assert mock_post.call_count == 1  # Only once
    # Verify username/password (lowercase field name per smoke script)
    body = mock_post.call_args.kwargs["json"]
    assert body == {"username": "admin", "password": "pw"}


@patch("pipelines.common.regscale.requests.post")
def test_authenticate_raises_on_missing_token(mock_post, mock_resp_factory):
    mock_post.return_value = mock_resp_factory({"id": 1})  # no auth_token
    c = RegScaleClient(
        url="http://10.10.30.28", username="admin", password="pw"
    )
    with pytest.raises(ValueError, match="auth_token"):
        c.authenticate()


@patch("pipelines.common.regscale.requests.get")
@patch("pipelines.common.regscale.requests.post")
def test_get_reauths_on_401(mock_post, mock_get, mock_resp_factory):
    mock_post.return_value = mock_resp_factory({"auth_token": "jwt-1"})
    unauthorized = mock_resp_factory({}, status=401)
    unauthorized.status_code = 401
    ok = mock_resp_factory({"ok": True})
    mock_get.side_effect = [unauthorized, ok]

    c = RegScaleClient(
        url="http://10.10.30.28", username="admin", password="pw"
    )
    c._token = "stale"  # pre-populate stale token
    body = c.get("/api/SeedingStatus")
    assert body == {"ok": True}
    # get called twice (401 then success), post called once (re-auth)
    assert mock_get.call_count == 2
    assert mock_post.call_count == 1


@patch("pipelines.common.regscale.requests.get")
@patch("pipelines.common.regscale.requests.post")
def test_seeding_status_round_trip(mock_post, mock_get, mock_resp_factory):
    mock_post.return_value = mock_resp_factory({"auth_token": "jwt"})
    mock_get.return_value = mock_resp_factory({"status": "complete"})
    c = RegScaleClient(
        url="http://10.10.30.28", username="admin", password="pw"
    )
    result = c.seeding_status()
    assert result["status"] == "complete"
    # URL should be the SeedingStatus endpoint
    called_url = mock_get.call_args.args[0]
    assert "SeedingStatus" in called_url
