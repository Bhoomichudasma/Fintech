from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def linear_regression_forecast(df: pd.DataFrame, days: int = 7) -> list[dict[str, float | str]]:
    closes = df["Close"].dropna()
    if len(closes) < 5:
        return []
    x = np.arange(len(closes))
    y = closes.values
    slope, intercept = np.polyfit(x, y, 1)
    last_index = x[-1]
    predictions = []
    for i in range(1, days + 1):
        idx = last_index + i
        predicted = intercept + slope * idx
        predictions.append(
            {
                "date": (datetime.utcnow() + timedelta(days=i)).isoformat(),
                "predicted_close": float(predicted),
            }
        )
    return predictions
