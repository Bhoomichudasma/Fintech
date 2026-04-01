from fastapi import APIRouter, HTTPException, Query
import traceback

from app.services.data_service import get_compare_data

router = APIRouter(prefix="/compare", tags=["compare"])


@router.get("")
async def compare(symbols: str = Query(..., description="Comma separated symbols")) -> dict:
    try:
        symbols_list = [sym.strip().upper() for sym in symbols.split(",") if sym.strip()]
        if not symbols_list:
            symbols_list = ["AAPL", "MSFT"]
        result = get_compare_data(symbols_list)
        return result.model_dump() if hasattr(result, "model_dump") else result.dict()
    except HTTPException:
        raise
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
