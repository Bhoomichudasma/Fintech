"""
Data service — OHLC: Alpha Vantage (primary) -> Yahoo chart API (fallback).
Finnhub free tier for 52-week metrics enrichment.
"""
from __future__ import annotations
import os
from typing import List
import pandas as pd
from fastapi import HTTPException
from app.models.schemas import (
    CompareItem, CompareResponse, Company, OHLCPoint,
    StockDataResponse, StockMetrics, StockPrediction, StockSummary,
)
from app.services.cache import cache
from app.services.metrics import compute_indicators, compute_summary
from app.services.news_service import fetch_news
from app.services.prediction import linear_regression_forecast
from app.utils.alternative_sources import (
    fetch_from_alpha_vantage, fetch_from_yahoo, fetch_finnhub_metrics,
)

ALPHAVANTAGE_KEY = os.getenv("ALPHAVANTAGE_KEY")
FINNHUB_KEY = os.getenv("FINNHUB_KEY")

_COMPANIES = [
    Company(symbol="AAPL", name="Apple"), Company(symbol="MSFT", name="Microsoft"),
    Company(symbol="GOOGL", name="Alphabet"), Company(symbol="AMZN", name="Amazon"),
    Company(symbol="TSLA", name="Tesla"), Company(symbol="META", name="Meta"),
    Company(symbol="NVDA", name="NVIDIA"), Company(symbol="NFLX", name="Netflix"),
    Company(symbol="JPM", name="JPMorgan"), Company(symbol="V", name="Visa"),
    Company(symbol="JNJ", name="Johnson & Johnson"), Company(symbol="WMT", name="Walmart"),
    Company(symbol="DIS", name="Disney"), Company(symbol="PYPL", name="PayPal"),
    Company(symbol="BABA", name="Alibaba"),
]

def range_to_days(range_param):
    return {"7d":7,"30d":30,"60d":60,"90d":90,"180d":180,"1y":365}.get(range_param, 30)

def _fetch_raw_df(symbol):
    ck = f"raw_df:{symbol}"
    cached = cache.get(ck)
    if cached is not None:
        return cached
    df = fetch_from_alpha_vantage(symbol, ALPHAVANTAGE_KEY or "", output_size="compact")
    if df is None or df.empty:
        print(f"[data_service] Alpha Vantage unavailable for {symbol}, using Yahoo chart API")
        df = fetch_from_yahoo(symbol, range_param="3mo")
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail=f"No data found for symbol: {symbol}")
    cache.set(ck, df)
    return df

def _fetch_df(symbol, days):
    return _fetch_raw_df(symbol).tail(days)

def _df_to_ohlc_points(df):
    points = []
    for idx, row in df.iterrows():
        points.append(OHLCPoint(
            date=idx, open=float(row["Open"]), high=float(row["High"]),
            low=float(row["Low"]), close=float(row["Close"]), volume=int(row["Volume"]),
            daily_return=float(row.get("DailyReturn", 0.0)),
            ma7=float(row.get("MA7", 0.0)), ma30=float(row.get("MA30", 0.0)),
        ))
    return points

def get_stock_data(symbol, range_param="30d"):
    days = range_to_days(range_param)
    ck = f"stock:{symbol}:{range_param}"
    cached = cache.get(ck)
    if cached is not None:
        return cached
    df = _fetch_df(symbol, days)
    df = compute_indicators(df)
    points = _df_to_ohlc_points(df)
    summary_dict = compute_summary(df)
    fh = fetch_finnhub_metrics(symbol, FINNHUB_KEY or "")
    high_52 = float(fh.get("52WeekHigh") or summary_dict["high_52_week"]) if fh else float(summary_dict["high_52_week"])
    low_52 = float(fh.get("52WeekLow") or summary_dict["low_52_week"]) if fh else float(summary_dict["low_52_week"])
    metrics = StockMetrics(
        volatility=summary_dict["volatility"], high_52_week=high_52, low_52_week=low_52,
        average_close=summary_dict["average_close"], momentum=summary_dict["momentum"],
        risk_level=summary_dict["risk_level"], health_score=summary_dict["health_score"],
        anomaly=summary_dict.get("anomaly"), volume_spike=summary_dict.get("volume_spike"),
        price_spike=summary_dict.get("price_spike"), move_reason=summary_dict.get("move_reason"),
    )
    predictions = [StockPrediction(date=p["date"], predicted_close=p["predicted_close"])
                   for p in linear_regression_forecast(df, days=7)]
    news = fetch_news(symbol)
    result = StockDataResponse(symbol=symbol, currency="USD", points=points,
                               metrics=metrics, predictions=predictions, news=news)
    cache.set(ck, result)
    return result

def _build_compare_item(symbol, df):
    s = compute_summary(df)
    item = CompareItem(symbol=symbol, average_close=s["average_close"],
                       volatility=s["volatility"], momentum=s["momentum"], health_score=s["health_score"])
    return item, df["Close"]

def get_compare_data(symbols):
    items, close_series = [], {}
    for symbol in symbols:
        ck = f"compare:{symbol}"
        hit = cache.get(ck)
        if hit:
            items.append(hit["item"]); close_series[symbol] = hit["close"]; continue
        raw_df = cache.get(f"raw_df:{symbol}")
        if raw_df is not None and not raw_df.empty:
            df = compute_indicators(raw_df.copy())
            item, closes = _build_compare_item(symbol, df)
            items.append(item); close_series[symbol] = closes
            cache.set(ck, {"item": item, "close": closes}); continue
        found = False
        for rng in ("30d", "90d", "7d"):
            sc = cache.get(f"stock:{symbol}:{rng}")
            if sc and sc.points:
                pts = sc.points
                closes = pd.Series([p.close for p in pts], index=pd.to_datetime([p.date for p in pts]))
                df_r = pd.DataFrame({"Close": closes, "Open": [p.open for p in pts],
                                     "High": [p.high for p in pts], "Low": [p.low for p in pts],
                                     "Volume": [p.volume for p in pts]})
                s = compute_summary(df_r)
                item = CompareItem(symbol=symbol, average_close=s["average_close"],
                                   volatility=s["volatility"], momentum=s["momentum"], health_score=s["health_score"])
                items.append(item); close_series[symbol] = closes
                cache.set(ck, {"item": item, "close": closes}); found = True; break
        if found:
            continue
        try:
            df = _fetch_raw_df(symbol)
            df = compute_indicators(df.copy())
            item, closes = _build_compare_item(symbol, df)
            items.append(item); close_series[symbol] = closes
            cache.set(ck, {"item": item, "close": closes})
        except Exception:
            continue
    if len(close_series) >= 2:
        closes_df = pd.DataFrame(close_series)
        corr = closes_df.corr()
        vs = list(close_series.keys())
        corr = corr.reindex(index=vs, columns=vs).fillna(0.0)
        matrix = [[round(float(v), 4) for v in row] for row in corr.values.tolist()]
    elif len(close_series) == 1:
        matrix = [[1.0]]
    else:
        matrix = []
    vs = [i.symbol for i in items]
    return CompareResponse(items=items, correlation_matrix=matrix, symbols=vs)

def list_companies():
    return _COMPANIES

def get_summary(symbol):
    ck = f"summary:{symbol}"
    cached = cache.get(ck)
    if cached is not None:
        return cached
    df = _fetch_df(symbol, 90)
    df = compute_indicators(df)
    s = compute_summary(df)
    fh = fetch_finnhub_metrics(symbol, FINNHUB_KEY or "")
    high_52 = float(fh.get("52WeekHigh") or s["high_52_week"]) if fh else float(s["high_52_week"])
    low_52 = float(fh.get("52WeekLow") or s["low_52_week"]) if fh else float(s["low_52_week"])
    result = StockSummary(symbol=symbol, high_52_week=high_52, low_52_week=low_52,
                          average_close=s["average_close"], volatility=s["volatility"],
                          momentum=s["momentum"], risk_level=s["risk_level"], health_score=s["health_score"])
    cache.set(ck, result)
    return result
