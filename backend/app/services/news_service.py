from __future__ import annotations

import os
from datetime import datetime, timedelta

import httpx

from app.services.cache import cache

NEWS_API_KEY = os.getenv("NEWSAPI_KEY")
FINNHUB_KEY = os.getenv("FINNHUB_KEY")
NEWS_URL = "https://newsapi.org/v2/everything"
FINNHUB_NEWS_URL = "https://finnhub.io/api/v1/company-news"


def fetch_news(symbol: str, limit: int = 5) -> list[dict]:
    cache_key = f"news:{symbol}:{limit}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    if not NEWS_API_KEY:
        # Fallback: use Finnhub /company-news — fetch extra to account for non-English filtering
        results = _fetch_from_finnhub(symbol, limit, fetch_limit=limit * 6)
        cache.set(cache_key, results)
        return results

    try:
        params = {
            "q": symbol,
            "pageSize": limit,
            "sortBy": "publishedAt",
            "apiKey": NEWS_API_KEY,
            "language": "en",
        }
        resp = httpx.get(NEWS_URL, params=params, timeout=8.0)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles", [])
        results = []
        for art in articles:
            results.append(
                {
                    "title": art.get("title", ""),
                    "url": art.get("url", ""),
                    "source": (art.get("source") or {}).get("name"),
                    "published_at": art.get("publishedAt"),
                }
            )
        cache.set(cache_key, results)
        return results
    except Exception:
        return []


def _is_english(text: str) -> bool:
    """Return True if text is likely English (all ASCII printable characters)."""
    if not text:
        return False
    try:
        text.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def _fetch_from_finnhub(symbol: str, limit: int, fetch_limit: int = 50) -> list[dict]:
    """Fetch company news from Finnhub /company-news endpoint, English only."""
    try:
        today = datetime.utcnow().date()
        from_date = (datetime.utcnow() - timedelta(days=7)).date()
        params = {
            "symbol": symbol,
            "from": str(from_date),
            "to": str(today),
            "token": FINNHUB_KEY or "",
        }
        resp = httpx.get(FINNHUB_NEWS_URL, params=params, timeout=8.0)
        resp.raise_for_status()
        articles = resp.json()
        results = []
        for art in articles[:fetch_limit]:
            if len(results) >= limit:
                break
            title = art.get("headline", "")
            if not _is_english(title):
                continue
            ts = art.get("datetime")
            published_at = datetime.utcfromtimestamp(ts).isoformat() if ts else None
            results.append({
                "title": title,
                "url": art.get("url", ""),
                "source": art.get("source"),
                "published_at": published_at,
            })
        return results
    except Exception:
        return []
