from fastapi import APIRouter, HTTPException

from app.services.data_service import get_summary

router = APIRouter(prefix="/summary", tags=["summary"])


@router.get("/{symbol}")
async def summary(symbol: str) -> dict:
    try:
        return get_summary(symbol)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc
