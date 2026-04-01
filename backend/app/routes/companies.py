from fastapi import APIRouter

from app.services.data_service import list_companies

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("")
async def get_companies() -> dict:
    return {"companies": list_companies()}
