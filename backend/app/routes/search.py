from fastapi import APIRouter, HTTPException, Query

from app.services.search_service import search_companies

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
async def search(q: str = Query(..., min_length=1, description="Company or symbol query")) -> dict:
    try:
        results = search_companies(q)
        return {"results": results}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
