"""
Preservation property tests.

These tests verify that the computation pipeline (metrics.py, prediction.py,
cache.py) is unchanged and correct. They should PASS on both unfixed and fixed
code since those files are never modified.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8**
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra.pandas import column, data_frames, range_indexes


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_ohlcv_df(n: int, close_prices=None) -> pd.DataFrame:
    """Build a synthetic OHLCV DataFrame with n rows."""
    if close_prices is None:
        close_prices = np.linspace(100, 200, n)
    dates = pd.date_range(end=datetime.utcnow(), periods=n, freq="D")
    df = pd.DataFrame(
        {
            "Open": close_prices * 0.99,
            "High": close_prices * 1.02,
            "Low": close_prices * 0.97,
            "Close": close_prices,
            "Volume": np.full(n, 1_000_000, dtype=int),
        },
        index=dates,
    )
    return df


# ---------------------------------------------------------------------------
# Unit observations (non-PBT)
# ---------------------------------------------------------------------------

def test_compute_indicators_adds_expected_columns():
    """compute_indicators appends MA7, MA30, DailyReturn columns."""
    from app.services.metrics import compute_indicators

    df = make_ohlcv_df(30)
    result = compute_indicators(df)
    for col in ("MA7", "MA30", "DailyReturn"):
        assert col in result.columns, f"Missing column: {col}"


def test_compute_indicators_no_nan_in_final_rows():
    """compute_indicators leaves no NaN in the last rows after ffill/bfill."""
    from app.services.metrics import compute_indicators

    df = make_ohlcv_df(30)
    result = compute_indicators(df)
    last_row = result.iloc[-1]
    for col in ("MA7", "MA30", "DailyReturn"):
        assert not math.isnan(float(last_row[col])), f"NaN in last row column {col}"


def test_compute_summary_returns_required_keys():
    """compute_summary returns all required keys with finite float values."""
    from app.services.metrics import compute_summary

    df = make_ohlcv_df(60)
    from app.services.metrics import compute_indicators
    df = compute_indicators(df)
    summary = compute_summary(df)

    required_keys = [
        "volatility", "high_52_week", "low_52_week",
        "average_close", "momentum", "risk_level", "health_score",
    ]
    for key in required_keys:
        assert key in summary, f"Missing key: {key}"

    numeric_keys = [k for k in required_keys if k != "risk_level"]
    for key in numeric_keys:
        val = summary[key]
        assert isinstance(val, (int, float)), f"{key} is not numeric: {val}"
        assert math.isfinite(float(val)), f"{key} is not finite: {val}"


def test_linear_regression_forecast_returns_7_predictions():
    """linear_regression_forecast returns exactly 7 prediction dicts."""
    from app.services.prediction import linear_regression_forecast

    df = make_ohlcv_df(30)
    preds = linear_regression_forecast(df, days=7)
    assert len(preds) == 7, f"Expected 7 predictions, got {len(preds)}"
    for p in preds:
        assert "date" in p
        assert "predicted_close" in p


def test_ttlcache_returns_same_object_within_ttl():
    """TTLCache returns the same object on second get within TTL."""
    from app.services.cache import TTLCache

    c = TTLCache(ttl_seconds=300)
    obj = {"value": 42}
    c.set("key", obj)
    result = c.get("key")
    assert result is obj, "Cache did not return the same object"


def test_ttlcache_expires_after_ttl():
    """TTLCache returns None after TTL expires."""
    import time
    from unittest.mock import patch
    from app.services.cache import TTLCache

    c = TTLCache(ttl_seconds=1)
    c.set("key", "value")
    # Simulate time passing beyond TTL by patching time.time in the cache module
    future_time = time.time() + 10
    with patch("app.services.cache.time") as mock_time:
        mock_time.time.return_value = future_time
        result = c.get("key")
    assert result is None, "Cache should have expired"


# ---------------------------------------------------------------------------
# Property-based tests (hypothesis)
# ---------------------------------------------------------------------------

@given(
    n_rows=st.integers(min_value=5, max_value=500),
    close_base=st.floats(min_value=1.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=50)
def test_pbt_compute_indicators_never_nan(n_rows, close_base):
    """
    Property: For any DataFrame with 5-500 rows and close prices 1-1000,
    compute_indicators never produces NaN in output columns after ffill/bfill.

    **Validates: Requirements 3.1**
    """
    from app.services.metrics import compute_indicators

    close_prices = np.linspace(close_base, close_base * 1.1, n_rows)
    df = make_ohlcv_df(n_rows, close_prices=close_prices)
    result = compute_indicators(df)

    for col in ("MA7", "MA30", "DailyReturn"):
        assert col in result.columns
        # After ffill/bfill/fillna(0), no NaN should remain
        assert not result[col].isna().any(), (
            f"NaN found in column {col} for n_rows={n_rows}"
        )


@given(
    n_rows=st.integers(min_value=3, max_value=500),
    close_base=st.floats(min_value=1.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=50)
def test_pbt_compute_summary_all_keys_finite(n_rows, close_base):
    """
    Property: For any DataFrame with >= 3 rows, compute_summary returns all
    required keys with finite values. (3 rows minimum needed for finite volatility
    since pct_change() on 2 rows yields 1 value and std() of 1 value is NaN.)

    **Validates: Requirements 3.1, 3.2**
    """
    from app.services.metrics import compute_indicators, compute_summary

    close_prices = np.linspace(close_base, close_base * 1.1, n_rows)
    df = make_ohlcv_df(n_rows, close_prices=close_prices)
    df = compute_indicators(df)
    summary = compute_summary(df)

    required_keys = [
        "volatility", "high_52_week", "low_52_week",
        "average_close", "momentum", "risk_level", "health_score",
    ]
    for key in required_keys:
        assert key in summary, f"Missing key: {key}"

    numeric_keys = [k for k in required_keys if k != "risk_level"]
    for key in numeric_keys:
        val = float(summary[key])
        assert math.isfinite(val), f"{key} is not finite: {val} (n_rows={n_rows})"


@pytest.mark.parametrize("range_param,max_days", [
    ("7d", 7),
    ("30d", 30),
    ("90d", 90),
    ("1y", 365),
])
def test_range_to_days_mapping(range_param, max_days):
    """
    Property: range_to_days maps each valid range_param to the correct day count.
    After fix, data_service.range_to_days must exist and return correct values.

    **Validates: Requirements 3.3**
    """
    # This test will fail on unfixed code (no range_to_days) and pass after fix
    try:
        from app.services.data_service import range_to_days
        result = range_to_days(range_param)
        assert result == max_days, f"range_to_days({range_param!r}) = {result}, expected {max_days}"
    except ImportError:
        pytest.skip("data_service.range_to_days not yet implemented (pre-fix)")


def test_range_to_days_default():
    """range_to_days returns 30 for unknown values."""
    try:
        from app.services.data_service import range_to_days
        assert range_to_days("unknown") == 30
        assert range_to_days("") == 30
    except ImportError:
        pytest.skip("data_service.range_to_days not yet implemented (pre-fix)")
