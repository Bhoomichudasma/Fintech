from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Company(BaseModel):
    symbol: str
    name: str


class OHLCPoint(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    daily_return: float = Field(..., description="Percentage daily return")
    ma7: float
    ma30: float


class StockMetrics(BaseModel):
    volatility: float
    high_52_week: float
    low_52_week: float
    average_close: float
    momentum: float
    risk_level: str
    health_score: float
    anomaly: str | None = None
    volume_spike: float | None = None
    price_spike: float | None = None
    move_reason: str | None = None


class StockPrediction(BaseModel):
    date: datetime
    predicted_close: float


class NewsItem(BaseModel):
    title: str
    url: str
    source: str | None = None
    published_at: datetime | None = None


class StockDataResponse(BaseModel):
    symbol: str
    currency: Optional[str]
    points: List[OHLCPoint]
    metrics: StockMetrics
    predictions: List[StockPrediction]
    news: List[NewsItem] | None = None


class StockSummary(BaseModel):
    symbol: str
    high_52_week: float
    low_52_week: float
    average_close: float
    volatility: float
    momentum: float
    risk_level: str
    health_score: float


class CompareItem(BaseModel):
    symbol: str
    average_close: float
    volatility: float
    momentum: float
    health_score: float


class CompareResponse(BaseModel):
    items: List[CompareItem]
    correlation_matrix: List[List[float]]
    symbols: List[str]
