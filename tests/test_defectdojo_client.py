"""Tests for pipelines.common.defectdojo -- DefectDojo API v2 client."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from pipelines.common.defectdojo import DefectDojoClient


@pytest.fixture
def mock_resp_factory():
    def _make(json_data: dict, status: int = 200) -> MagicMock:
        m = MagicMock()
        m.status_code = status
        m.json.return_value = json_data
        m.raise_for_status.return_value = None
        return m

    return _make


@patch("pipelines.common.defectdojo.requests.get")
def test_list_products_returns_results(mock_get, mock_resp_factory):
    # ADR 0006 amendment: ASCII hyphens, not em dashes
    mock_get.return_value = mock_resp_factory(
        {
            "results": [
                {"id": 1, "name": "MSS Core - brisket"},
                {"id": 2, "name": "MSS Log Analytics - haccp"},
            ]
        }
    )
    c = DefectDojoClient(url="http://10.10.30.27:8080", api_key="x")
    products = c.list_products()
    assert len(products) == 2
    assert products[0]["name"] == "MSS Core - brisket"


@patch("pipelines.common.defectdojo.requests.get")
def test_list_products_uses_token_header(mock_get, mock_resp_factory):
    mock_get.return_value = mock_resp_factory({"results": []})
    c = DefectDojoClient(url="http://10.10.30.27:8080", api_key="SECRET")
    c.list_products()
    kwargs = mock_get.call_args.kwargs
    assert kwargs["headers"]["Authorization"] == "Token SECRET"


@patch("pipelines.common.defectdojo.requests.get")
def test_list_engagements_by_product(mock_get, mock_resp_factory):
    mock_get.return_value = mock_resp_factory(
        {"results": [{"id": 10, "name": "ConMon 2026-04", "product": 1}]}
    )
    c = DefectDojoClient(url="http://10.10.30.27:8080", api_key="x")
    engagements = c.list_engagements(product_id=1)
    assert engagements[0]["name"] == "ConMon 2026-04"
    assert mock_get.call_args.kwargs["params"] == {"product": 1}


@patch("pipelines.common.defectdojo.requests.post")
def test_create_engagement_posts_required_fields(mock_post, mock_resp_factory):
    mock_post.return_value = mock_resp_factory(
        {"id": 42, "name": "ConMon 2026-04", "product": 1}
    )
    c = DefectDojoClient(url="http://10.10.30.27:8080", api_key="x")
    result = c.create_engagement(product_id=1, name="ConMon 2026-04")
    assert result["id"] == 42
    body = mock_post.call_args.kwargs["json"]
    assert body["name"] == "ConMon 2026-04"
    assert body["product"] == 1
    assert body["status"] == "In Progress"
    assert body["engagement_type"] == "CI/CD"
    assert body["target_start"]
    assert body["target_end"]


@patch("pipelines.common.defectdojo.requests.post")
def test_import_generic_findings(mock_post, mock_resp_factory):
    mock_post.return_value = mock_resp_factory(
        {"test_id": 123, "engagement_id": 7}
    )
    c = DefectDojoClient(url="http://10.10.30.27:8080", api_key="x")
    result = c.import_generic_findings(
        engagement_id=7,
        scan_type="Generic Findings Import",
        findings_json={"findings": []},
    )
    assert result["test_id"] == 123
    # Ensure multipart form data was posted (files= present)
    assert "files" in mock_post.call_args.kwargs
    form = mock_post.call_args.kwargs["data"]
    assert form["engagement"] == 7
    assert form["scan_type"] == "Generic Findings Import"


@patch("pipelines.common.defectdojo.requests.get")
def test_list_findings_auto_paginates(mock_get, mock_resp_factory):
    """DefectDojo caps each page at 1000; list_findings must walk
    pages until next=null."""
    page1 = mock_resp_factory(
        {
            "count": 2500,
            "next": "http://x/api/v2/findings/?offset=1000",
            "previous": None,
            "results": [{"id": i} for i in range(1000)],
        }
    )
    page2 = mock_resp_factory(
        {
            "count": 2500,
            "next": "http://x/api/v2/findings/?offset=2000",
            "previous": None,
            "results": [{"id": i} for i in range(1000, 2000)],
        }
    )
    page3 = mock_resp_factory(
        {
            "count": 2500,
            "next": None,
            "previous": None,
            "results": [{"id": i} for i in range(2000, 2500)],
        }
    )
    mock_get.side_effect = [page1, page2, page3]

    c = DefectDojoClient(url="http://10.10.30.27:8080", api_key="x")
    rows = c.list_findings()

    assert len(rows) == 2500
    assert mock_get.call_count == 3


@patch("pipelines.common.defectdojo.requests.get")
def test_list_findings_respects_max_pages(mock_get, mock_resp_factory):
    page = mock_resp_factory(
        {
            "count": 5000,
            "next": "http://x/api/v2/findings/?offset=1000",
            "previous": None,
            "results": [{"id": i} for i in range(1000)],
        }
    )
    mock_get.return_value = page

    c = DefectDojoClient(url="http://10.10.30.27:8080", api_key="x")
    rows = c.list_findings(max_pages=2)
    assert len(rows) == 2000
    assert mock_get.call_count == 2
