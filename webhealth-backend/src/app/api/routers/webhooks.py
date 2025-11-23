from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/test")
async def trigger_test_webhook() -> dict[str, str]:
    return {"detail": "Webhook delivery not implemented"}
