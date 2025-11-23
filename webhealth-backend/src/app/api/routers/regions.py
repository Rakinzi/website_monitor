from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/regions", tags=["regions"])


@router.get("/")
async def list_regions() -> dict[str, str]:
    return {"detail": "Region API not implemented yet"}
