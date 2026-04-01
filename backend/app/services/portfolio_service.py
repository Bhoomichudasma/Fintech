"""
Portfolio simulation service.
"""
from __future__ import annotations

from typing import List

import pandas as pd
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.db_models import Portfolio, PortfolioHolding, PortfolioRun


def simulate_portfolio(
    holdings: List[dict],  # [{symbol, weight}]
    initial: float,
    range_param: str = "180d",
) -> dict:
    """
    Simulate portfolio performance over the given range.
    Returns { total_return_pct: float, points: [{date, value}] }
    """
    # Import here to avoid circular imports at module load time
    from app.services.data_service import _fetch_raw_df

    _range_map = {"7d": 7, "30d": 30, "60d": 60, "90d": 90, "180d": 180, "1y": 365}
    days = _range_map.get(range_param, 180)

    valid = [h for h in holdings if str(h.get("symbol", "")).strip()]
    if not valid:
        raise HTTPException(status_code=400, detail="No valid holdings provided")

    total_weight = sum(float(h.get("weight", 1)) for h in valid)
    if total_weight == 0:
        raise HTTPException(status_code=400, detail="Total weight cannot be zero")

    close_frames: dict[str, pd.Series] = {}
    for h in valid:
        symbol = str(h["symbol"]).strip().upper()
        try:
            df = _fetch_raw_df(symbol)
            close_frames[symbol] = df["Close"].tail(days).rename(symbol)
        except HTTPException:
            continue

    if not close_frames:
        raise HTTPException(status_code=404, detail="Could not fetch data for any holding")

    closes = pd.DataFrame(close_frames).dropna(how="all").ffill().bfill()
    rebased = closes / closes.iloc[0]

    portfolio_value = pd.Series(0.0, index=rebased.index)
    for h in valid:
        symbol = str(h["symbol"]).strip().upper()
        if symbol not in rebased.columns:
            continue
        weight = float(h.get("weight", 1)) / total_weight
        portfolio_value += rebased[symbol] * (initial * weight)

    total_return_pct = float(
        (portfolio_value.iloc[-1] - portfolio_value.iloc[0]) / portfolio_value.iloc[0] * 100
    )

    points = [
        {"date": idx.isoformat(), "value": round(float(val), 2)}
        for idx, val in portfolio_value.items()
    ]

    return {
        "total_return_pct": round(total_return_pct, 4),
        "points": points,
    }


def record_portfolio_run(
    name: str,
    holdings: List[dict],
    initial: float,
    range_param: str,
    result: dict,
    db: Session,
) -> PortfolioRun:
    """Persist a simulation run so the database always has user activity."""
    valid_holdings = [
        {"symbol": str(h.get("symbol", "")).strip().upper(), "weight": float(h.get("weight", 1))}
        for h in holdings
        if str(h.get("symbol", "")).strip()
    ]
    run = PortfolioRun(
        name=(name or "Portfolio Simulation").strip() or "Portfolio Simulation",
        initial=initial,
        range=range_param,
        holdings=valid_holdings,
        result=result,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def save_portfolio(
    name: str,
    holdings: List[dict],
    initial: float,
    range_param: str,
    db: Session,
) -> Portfolio:
    """Persist a portfolio and its holdings in PostgreSQL."""
    valid = [h for h in holdings if str(h.get("symbol", "")).strip()]
    if not valid:
        raise HTTPException(status_code=400, detail="No valid holdings provided")

    portfolio = Portfolio(name=name.strip() or "Untitled", initial=initial, range=range_param)
    portfolio.holdings = [
        PortfolioHolding(symbol=str(h["symbol"]).strip().upper(), weight=float(h.get("weight", 1)))
        for h in valid
    ]
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


def list_portfolios(db: Session) -> List[Portfolio]:
    return db.query(Portfolio).order_by(Portfolio.created_at.desc()).all()


def get_portfolio_by_id(portfolio_id: int, db: Session) -> Portfolio:
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    # eager load holdings while session is open
    _ = portfolio.holdings  # noqa: WPS122
    return portfolio
