from __future__ import annotations

from dotenv import load_dotenv
load_dotenv(override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_db
from app.routes.companies import router as companies_router
from app.routes.data import router as data_router
from app.routes.compare import router as compare_router
from app.routes.search import router as search_router
from app.routes.summary import router as summary_router
from app.routes.portfolio import router as portfolio_router

app = FastAPI(title="Stock Market Dashboard API")

# Ensure database tables exist at startup (no-op if already created)
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies_router)
app.include_router(data_router)
app.include_router(compare_router)
app.include_router(search_router)
app.include_router(summary_router)
app.include_router(portfolio_router)
