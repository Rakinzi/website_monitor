from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_notification_service,
    get_settings_service,
)
from app.schemas.settings_schemas import SettingsOut, SettingsUpdate
from app.schemas.escalation_schemas import (
    EscalationPolicyCreate,
    EscalationPolicyOut,
    EscalationPolicyUpdate,
)
from app.services.notification_service import NotificationService
from app.services.settings_service import SettingsService

router = APIRouter(prefix="/settings", tags=["settings"])

SettingsServiceDep = Annotated[SettingsService, Depends(get_settings_service)]
NotificationDep = Annotated[NotificationService, Depends(get_notification_service)]


@router.get("/", response_model=SettingsOut)
async def get_settings(service: SettingsServiceDep) -> SettingsOut:
    return await service.get_settings()


@router.put("/", response_model=SettingsOut)
async def update_settings(
    payload: SettingsUpdate,
    service: SettingsServiceDep,
) -> SettingsOut:
    return await service.update_settings(payload)


@router.get("/escalations", response_model=List[EscalationPolicyOut])
async def list_escalations(service: SettingsServiceDep) -> List[EscalationPolicyOut]:
    return await service.list_escalations()


@router.post("/escalations", response_model=EscalationPolicyOut, status_code=status.HTTP_201_CREATED)
async def create_escalation(
    payload: EscalationPolicyCreate,
    service: SettingsServiceDep,
) -> EscalationPolicyOut:
    return await service.create_escalation(payload)


@router.put("/escalations/{policy_id}", response_model=EscalationPolicyOut)
async def update_escalation(
    policy_id: int,
    payload: EscalationPolicyUpdate,
    service: SettingsServiceDep,
) -> EscalationPolicyOut:
    policy = await service.update_escalation(policy_id, payload)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Escalation policy not found")
    return policy


@router.delete("/escalations/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_escalation(policy_id: int, service: SettingsServiceDep) -> None:
    deleted = await service.delete_escalation(policy_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Escalation policy not found")


@router.post("/webhook/test")
async def test_webhook(
    payload: dict,
    service: SettingsServiceDep,
    notifier: NotificationDep,
) -> dict[str, str]:
    url = payload.get("url")
    if not url:
        settings = await service.get_settings()
        url = settings.webhook_url
    if not url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Webhook URL required")
    await notifier.send_webhook(url, {"event": "webhealth_test", "status": "ok"})
    return {"detail": "Webhook test sent"}
