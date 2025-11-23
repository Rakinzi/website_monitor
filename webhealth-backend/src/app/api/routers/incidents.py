from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("/")
async def list_incidents() -> dict[str, str]:
    return {"detail": "Incident listing not implemented"}
