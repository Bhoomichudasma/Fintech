from __future__ import annotations

import numpy as np
import pandas as pd


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["DailyReturn"] = df["Close"].pct_change() * 100
    df["MA7"] = df["Close"].rolling(window=7).mean()
    df["MA30"] = df["Close"].rolling(window=30).mean()
    df["Volatility"] = df["DailyReturn"].rolling(window=30).std()
    # Clean NaN/inf so JSON stays valid
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    df.fillna(0, inplace=True)
    return df


def compute_summary(df: pd.DataFrame) -> dict[str, float | str]:
    closes = df["Close"].dropna()
    daily_return = (closes.pct_change() * 100).dropna()
    high_52 = closes.tail(252).max()
    low_52 = closes.tail(252).min()
    avg_close = closes.mean()
    volatility = daily_return.std() if not daily_return.empty else 0.0
    momentum = (closes.iloc[-1] - closes.iloc[-30]) / closes.iloc[-30] * 100 if len(closes) > 30 else 0.0
    risk_level = classify_risk(volatility)
    health_score = stock_health_score(avg_close, volatility, momentum)

    anomaly, price_spike, volume_spike = detect_anomaly(df)
    move_reason = explain_move(momentum, price_spike, volume_spike)
    return {
        "high_52_week": float(high_52),
        "low_52_week": float(low_52),
        "average_close": float(avg_close),
        "volatility": float(volatility),
        "momentum": float(momentum),
        "risk_level": risk_level,
        "health_score": float(health_score),
        "anomaly": anomaly,
        "price_spike": price_spike,
        "volume_spike": volume_spike,
        "move_reason": move_reason,
    }


def classify_risk(volatility: float) -> str:
    if volatility < 1.5:
        return "Low"
    if volatility < 3.0:
        return "Medium"
    return "High"


def stock_health_score(avg_close: float, volatility: float, momentum: float) -> float:
    vol_score = max(0.0, 100 - min(volatility * 10, 100))
    momentum_score = np.clip(momentum + 50, 0, 100)
    price_score = 60 if avg_close > 0 else 30
    return float(np.clip((vol_score * 0.4) + (momentum_score * 0.4) + (price_score * 0.2), 0, 100))


def detect_anomaly(df: pd.DataFrame) -> tuple[str | None, float | None, float | None]:
    if df.empty:
        return None, None, None
    closes = df["Close"].dropna()
    vols = df["Volume"].dropna()
    price_change = closes.pct_change().iloc[-1] * 100 if len(closes) > 1 else 0.0
    vol_mean = vols.rolling(window=20).mean().iloc[-1] if len(vols) >= 20 else vols.mean()
    vol_spike = (vols.iloc[-1] / vol_mean) if vol_mean else 1.0

    price_std = closes.pct_change().std() * 100 if len(closes) > 2 else 0.0
    price_spike = price_change / price_std if price_std else price_change

    if abs(price_change) > 3 and vol_spike > 2:
        return "Unusual move", price_change, vol_spike
    if vol_spike > 3:
        return "Volume spike", price_change, vol_spike
    if abs(price_change) > 3:
        return "Price spike", price_change, vol_spike
    return None, price_change, vol_spike


def explain_move(momentum: float, price_spike: float | None, volume_spike: float | None) -> str | None:
    if price_spike is None or volume_spike is None:
        return None
    reasons = []
    if price_spike > 3:
        reasons.append("Strong upward price swing")
    elif price_spike < -3:
        reasons.append("Sharp downward move")
    if volume_spike and volume_spike > 2:
        reasons.append("Volume surge above normal")
    if momentum > 5:
        reasons.append("Positive momentum streak")
    elif momentum < -5:
        reasons.append("Negative momentum streak")
    return "; ".join(reasons) or None
