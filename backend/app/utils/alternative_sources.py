from __future__ import annotations

import pandas as pd
import httpx


def fetch_from_alpha_vantage(symbol: str, api_key: str, output_size: str = "compact") -> pd.DataFrame | None:
    """Fetch OHLCV data from Alpha Vantage TIME_SERIES_DAILY."""
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": api_key,
            "outputsize": output_size,
            "datatype": "json",
        }
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        # Handle both rate-limit message keys
        if "Note" in data or "Information" in data:
            msg = data.get("Note") or data.get("Information", "")
            print(f"Alpha Vantage rate limited: {msg}")
            return None

        time_series = data.get("Time Series (Daily)", {})
        if not time_series:
            return None

        df_data = []
        for values in time_series.values():
            df_data.append({
                "Open": float(values["1. open"]),
                "High": float(values["2. high"]),
                "Low": float(values["3. low"]),
                "Close": float(values["4. close"]),
                "Volume": int(values["5. volume"]),
            })

        dates = pd.to_datetime(list(time_series.keys()))
        df = pd.DataFrame(df_data, index=dates)
        return df.sort_index()

    except Exception as e:
        print(f"Alpha Vantage failed: {e}")
        return None


def fetch_from_yahoo(symbol: str, range_param: str = "3mo") -> pd.DataFrame | None:
    """
    Fetch OHLCV data from Yahoo Finance v8 chart API.
    No API key required — free, no rate limit.
    range_param: 1mo, 3mo, 6mo, 1y, 2y
    """
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        params = {"interval": "1d", "range": range_param}
        headers = {"User-Agent": "Mozilla/5.0"}
        with httpx.Client(timeout=10.0) as client:
            r = client.get(url, params=params, headers=headers)
            r.raise_for_status()
            data = r.json()

        result = data.get("chart", {}).get("result", [])
        if not result:
            return None
        result = result[0]

        timestamps = result.get("timestamp", [])
        quote = result.get("indicators", {}).get("quote", [{}])[0]

        opens = quote.get("open", [])
        highs = quote.get("high", [])
        lows = quote.get("low", [])
        closes = quote.get("close", [])
        volumes = quote.get("volume", [])

        if not closes:
            return None

        # Build tz-naive DatetimeIndex from unix timestamps
        index = pd.to_datetime(timestamps, unit="s", utc=True).tz_convert(None)
        df = pd.DataFrame(
            {"Open": opens, "High": highs, "Low": lows, "Close": closes, "Volume": volumes},
            index=index,
        )
        df = df.dropna(subset=["Close"])
        return df.sort_index()

    except Exception as e:
        print(f"Yahoo chart API failed: {e}")
        return None


def fetch_finnhub_quote(symbol: str, api_key: str) -> dict | None:
    """
    Fetch real-time quote from Finnhub (free tier).
    Returns {c, d, dp, h, l, o, pc} or None if price is zero.
    """
    try:
        url = "https://finnhub.io/api/v1/quote"
        with httpx.Client(timeout=8.0) as client:
            r = client.get(url, params={"symbol": symbol, "token": api_key})
            r.raise_for_status()
            data = r.json()
        if data.get("c", 0) == 0:
            return None
        return data
    except Exception as e:
        print(f"Finnhub quote failed: {e}")
        return None


def fetch_finnhub_metrics(symbol: str, api_key: str) -> dict | None:
    """
    Fetch fundamental metrics from Finnhub (free tier).
    Returns the 'metric' dict containing 52WeekHigh, 52WeekLow, etc.
    """
    try:
        url = "https://finnhub.io/api/v1/stock/metric"
        with httpx.Client(timeout=8.0) as client:
            r = client.get(url, params={"symbol": symbol, "metric": "all", "token": api_key})
            r.raise_for_status()
            data = r.json()
        return data.get("metric") or None
    except Exception as e:
        print(f"Finnhub metrics failed: {e}")
        return None
