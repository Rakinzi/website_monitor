from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/uptime")
async def get_uptime_placeholder() -> dict[str, str]:
    return {"detail": "Analytics coming soon"}
