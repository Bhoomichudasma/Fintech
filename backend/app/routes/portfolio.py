from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List
import traceback

from sqlalchemy.orm import Session

from app.db import get_db
from app.models.db_models import PortfolioRun
from app.services.portfolio_service import (
    simulate_portfolio,
    record_portfolio_run,
    save_portfolio,
    list_portfolios,
    get_portfolio_by_id,
)

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


class Holding(BaseModel):
    symbol: str
    weight: float = 1.0


class PortfolioRequest(BaseModel):
    holdings: List[Holding]
    initial: float = 10000
    range: str = "90d"


class PortfolioSaveRequest(PortfolioRequest):
    name: str = Field(..., min_length=1, description="Label for the portfolio")


class PortfolioSummary(BaseModel):
    id: int
    name: str
    initial: float
    range: str
    holdings: List[Holding]
    created_at: str


@router.post("")
async def portfolio(req: PortfolioRequest, db: Session = Depends(get_db)):
    try:
        holdings_dicts = [{"symbol": h.symbol, "weight": h.weight} for h in req.holdings]
        result = simulate_portfolio(holdings_dicts, req.initial, req.range)
        run = record_portfolio_run("Portfolio Simulation", holdings_dicts, req.initial, req.range, result, db)
        return {**result, "run_id": run.id}
    except HTTPException:
        raise
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/save")
async def save(req: PortfolioSaveRequest, db: Session = Depends(get_db)) -> dict:
    try:
        holdings_dicts = [{"symbol": h.symbol, "weight": h.weight} for h in req.holdings]
        portfolio = save_portfolio(req.name, holdings_dicts, req.initial, req.range, db)
        return {"id": portfolio.id}
    except HTTPException:
        raise
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/saved")
async def saved(db: Session = Depends(get_db)) -> dict:
    portfolios = list_portfolios(db)
    results = []
    for p in portfolios:
        results.append({
            "id": p.id,
            "name": p.name,
            "initial": p.initial,
            "range": p.range,
            "holdings": [
                {"symbol": h.symbol, "weight": h.weight}
                for h in (p.holdings or [])
            ],
            "created_at": p.created_at.isoformat() if p.created_at else None,
        })
    return {"portfolios": results}


@router.get("/runs")
async def runs(db: Session = Depends(get_db)) -> dict:
    rows = db.query(PortfolioRun).order_by(PortfolioRun.created_at.desc()).all()
    return {
        "runs": [
            {
                "id": row.id,
                "name": row.name,
                "initial": row.initial,
                "range": row.range,
                "holdings": row.holdings,
                "result": row.result,
                "created_at": row.created_at.isoformat() if row.created_at else None,
            }
            for row in rows
        ]
    }


@router.get("/{portfolio_id}")
async def get_portfolio(portfolio_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        portfolio = get_portfolio_by_id(portfolio_id, db)
        return {
            "id": portfolio.id,
            "name": portfolio.name,
            "initial": portfolio.initial,
            "range": portfolio.range,
            "holdings": [
                {"symbol": h.symbol, "weight": h.weight}
                for h in (portfolio.holdings or [])
            ],
            "created_at": portfolio.created_at.isoformat() if portfolio.created_at else None,
        }
    except HTTPException:
        raise
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
