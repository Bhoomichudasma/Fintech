from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import relationship

from app.db import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    initial = Column(Float, nullable=False, default=10000.0)
    range = Column(String(16), nullable=False, default="90d")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    holdings = relationship(
        "PortfolioHolding",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class PortfolioHolding(Base):
    __tablename__ = "portfolio_holdings"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"))
    symbol = Column(String(32), nullable=False)
    weight = Column(Float, nullable=False, default=1.0)

    portfolio = relationship("Portfolio", back_populates="holdings")


class PortfolioRun(Base):
    __tablename__ = "portfolio_runs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    initial = Column(Float, nullable=False, default=10000.0)
    range = Column(String(16), nullable=False, default="90d")
    holdings = Column(JSON, nullable=False)
    result = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
