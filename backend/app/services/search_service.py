from __future__ import annotations

import os

import httpx

from app.services.cache import cache

FINNHUB_KEY = os.getenv("FINNHUB_KEY")
SEARCH_URL = "https://finnhub.io/api/v1/search"


def search_companies(query: str, limit: int = 10) -> list[dict[str, str]]:
    query = query.strip()
    if not query:
        return []

    cache_key = f"search:{query.lower()}:{limit}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        params = {"q": query, "token": FINNHUB_KEY or ""}
        resp = httpx.get(SEARCH_URL, params=params, timeout=5.0)
        resp.raise_for_status()
        data = resp.json()
        quotes = data.get("result", [])
        results = []
        for q in quotes[:limit]:
            symbol = q.get("displaySymbol") or q.get("symbol")
            name = q.get("description") or symbol
            exchange = q.get("type") or ""
            if not symbol:
                continue
            results.append(
                {
                    "symbol": symbol,
                    "name": name or symbol,
                    "exchange": exchange,
                }
            )
        cache.set(cache_key, results)
        return results
    except Exception:
        return []
