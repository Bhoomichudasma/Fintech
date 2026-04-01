from fastapi import APIRouter, HTTPException, Query
import traceback

from app.services.data_service import get_stock_data

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/{symbol}")
async def get_data(symbol: str, range: str = Query("30d", alias="range")) -> dict:
    try:
        data = get_stock_data(symbol, range)
        return data.model_dump() if hasattr(data, "model_dump") else data.dict()
    except HTTPException:
        raise
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
