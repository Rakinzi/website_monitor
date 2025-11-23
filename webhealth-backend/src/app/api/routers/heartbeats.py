from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/heartbeats", tags=["heartbeats"])


@router.post("/{token}")
async def process_heartbeat(token: str) -> dict[str, str]:
    return {"detail": f"Heartbeat {token} accepted (not implemented)"}
