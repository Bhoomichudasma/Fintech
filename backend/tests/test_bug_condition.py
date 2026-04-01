"""
Bug condition exploration tests.

These tests confirm the bugs exist on UNFIXED code.
On unfixed code: Tests 1-4 confirm bug conditions.
After fix (task 3.6): All four tests should PASS with correct behavior.

**Validates: Requirements 1.1, 1.2, 1.5, 1.7, 1.8, 1.9**
"""
from __future__ import annotations

import importlib
import os
import sys
import types
import unittest.mock as mock

import pytest


# ---------------------------------------------------------------------------
# Test 1: data_service.get_stock_data is missing (empty file)
# ---------------------------------------------------------------------------

def test_data_service_get_stock_data_exists_and_returns_response():
    """
    Bug condition: data_service.py IS empty — get_stock_data does not exist.
    Fixed behavior: get_stock_data("AAPL", "30d") returns a StockDataResponse
    with non-empty points.

    On UNFIXED code this test FAILS (AttributeError / no function).
    After fix this test PASSES.
    """
    import os
    from pathlib import Path
    from dotenv import load_dotenv

    # Load .env so API keys are available
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path, override=True)

    # Force fresh import after env is loaded
    for mod in list(sys.modules.keys()):
        if "data_service" in mod:
            del sys.modules[mod]

    import importlib
    import app.services.data_service as ds_mod
    importlib.reload(ds_mod)

    # Bug condition: function should not exist on unfixed code
    assert hasattr(ds_mod, "get_stock_data"), (
        "BUG CONFIRMED: data_service.get_stock_data does not exist — data_service.py is empty"
    )

    # After fix: calling it should return a StockDataResponse with points
    result = ds_mod.get_stock_data("AAPL", "30d")
    assert result is not None, "get_stock_data returned None"
    assert hasattr(result, "points"), "result has no 'points' attribute"
    assert len(result.points) > 0, "result.points is empty"


# ---------------------------------------------------------------------------
# Test 2: main.py has no routes — GET /companies returns 404
# ---------------------------------------------------------------------------

def test_companies_endpoint_returns_200():
    """
    Bug condition: main.py IS empty — no routes registered.
    Fixed behavior: GET /companies returns 200 with a companies list.

    On UNFIXED code this test FAILS (404 or import error).
    After fix this test PASSES.
    """
    # Force fresh import of main
    for mod in list(sys.modules.keys()):
        if mod in ("app.main", "main"):
            del sys.modules[mod]

    from fastapi.testclient import TestClient  # noqa: PLC0415

    from app.main import app  # noqa: PLC0415

    client = TestClient(app)
    response = client.get("/companies")

    assert response.status_code == 200, (
        f"BUG CONFIRMED: GET /companies returned {response.status_code} — main.py has no routes"
    )
    data = response.json()
    assert "companies" in data, "Response missing 'companies' key"
    assert len(data["companies"]) > 0, "companies list is empty"


# ---------------------------------------------------------------------------
# Test 3: search_service.SEARCH_URL contains "yahoo.com"
# ---------------------------------------------------------------------------

def test_search_url_does_not_contain_yahoo():
    """
    Bug condition: search_service uses Yahoo Finance URL.
    Fixed behavior: SEARCH_URL points to Finnhub, not yahoo.com.

    On UNFIXED code this test FAILS (SEARCH_URL contains yahoo.com).
    After fix this test PASSES.
    """
    for mod in list(sys.modules.keys()):
        if "search_service" in mod:
            del sys.modules[mod]

    from app.services import search_service  # noqa: PLC0415

    url = search_service.SEARCH_URL
    assert "yahoo.com" not in url, (
        f"BUG CONFIRMED: SEARCH_URL contains 'yahoo.com': {url}"
    )
    assert "finnhub.io" in url, (
        f"Expected SEARCH_URL to point to finnhub.io, got: {url}"
    )


# ---------------------------------------------------------------------------
# Test 4: fetch_news with NEWSAPI_KEY=None returns mock data (MockWire)
# ---------------------------------------------------------------------------

def test_fetch_news_without_newsapi_key_uses_finnhub_not_mock():
    """
    Bug condition: news_service returns mock data when NEWSAPI_KEY is absent.
    Fixed behavior: fetch_news uses Finnhub /company-news and returns real items
    where source != "MockWire".

    On UNFIXED code this test FAILS (source == "MockWire").
    After fix this test PASSES.
    """
    for mod in list(sys.modules.keys()):
        if "news_service" in mod:
            del sys.modules[mod]

    # Patch env so NEWSAPI_KEY is absent
    with mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop("NEWSAPI_KEY", None)

        # Re-import with patched env
        import importlib  # noqa: PLC0415

        import app.services.news_service as ns_mod  # noqa: PLC0415

        importlib.reload(ns_mod)

        # Patch httpx.get to return a fake Finnhub response so we don't hit real API
        fake_articles = [
            {
                "headline": "AAPL hits new high",
                "url": "https://finnhub.io/news/1",
                "source": "Reuters",
                "datetime": 1700000000,
                "summary": "",
            }
        ]

        with mock.patch("httpx.get") as mock_get:
            mock_resp = mock.MagicMock()
            mock_resp.raise_for_status.return_value = None
            mock_resp.json.return_value = fake_articles
            mock_get.return_value = mock_resp

            # Clear cache to force fresh fetch
            from app.services.cache import cache  # noqa: PLC0415
            cache._store.clear()

            result = ns_mod.fetch_news("AAPL", limit=5)

        assert len(result) > 0, "fetch_news returned empty list"
        sources = [item.get("source") for item in result]
        assert "MockWire" not in sources, (
            f"BUG CONFIRMED: fetch_news returned MockWire source — still using mock fallback. Sources: {sources}"
        )
