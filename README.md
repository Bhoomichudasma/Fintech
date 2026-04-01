# Stock Data Intelligence Dashboard

A mini Bloomberg-style analytics experience with FastAPI + React, live stock metrics, AI-assisted outlook, and playful simulations.

## Features

- FastAPI backend with yfinance-powered OHLC data, summaries, and comparisons.
- Calculated indicators: daily return, 7/30-day moving averages, volatility, 52-week high/low, momentum, risk level, and a custom Stock Health Score.
- AI linear-regression forecast for the next 7 days.
- Comparison API with correlation matrix across symbols.
- React + Vite + Tailwind dark fintech UI: sidebar watchlist, interactive charts, heatmap, risk meter, and "If you invested ₹10,000" simulator.
- Top gainers/losers surfaced from momentum; toggle overlays for MA and predictions.

## Project Structure

```
backend/
  app/
    main.py
    routes/
    services/
    models/
    utils/
frontend/
  src/
    pages/
    components/
    styles/
```

## Backend Setup

1. Create a virtual environment and install dependencies:
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
2. Run the API:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### API Endpoints

- `GET /companies` – list available symbols.
- `GET /data/{symbol}?range=30d` – OHLC + indicators + 7-day forecast.
- `GET /summary/{symbol}` – 52-week high/low, avg close, volatility, momentum, risk, health score.
- `GET /compare?symbols=INFY,TCS,RELIANCE` – comparison cards + correlation matrix.
- `POST /portfolio` – simulate a custom portfolio over a range.
- `POST /portfolio/save` – store a named portfolio (uses PostgreSQL).
- `GET /portfolio/runs` – inspect automatic simulation history saved to PostgreSQL.
- `GET /portfolio/saved` – list saved portfolios with holdings.
- `GET /portfolio/{id}` – retrieve a saved portfolio by id.
- `GET /health` – service check.

## Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Create `.env` (optional) to point to the backend:
   ```bash
   VITE_API_URL=http://localhost:8000
   ```
3. Run the dev server:
   ```bash
   npm run dev
   ```

## Notes 

- Symbols are seeded with popular US and Indian tickers
- Caching: simple in-memory TTL (5 minutes) keeps responses snappy
- PostgreSQL: set `DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/fintech` (defaults to localhost) to persist saved portfolios; tables auto-create at app start.
- Forecasts use a light linear regression via NumPy for fast responses; not investment advice.
- Need speed and no network? Set `FAST_MOCK=1` in the backend environment to serve synthetic but consistent data (per-symbol) instantly, skipping external calls.

## Deployment Tips

- For production, pin a process manager (e.g., gunicorn with uvicorn workers) and serve the frontend as static assets behind a reverse proxy.
- Add HTTPS, auth, and rate limiting before exposing publicly.
- Consider a task queue + scheduled jobs if precomputing indicators for many tickers.
