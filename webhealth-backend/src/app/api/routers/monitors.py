from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_user, get_monitor_service
from app.schemas.monitor_schemas import MonitorCreate, MonitorOut, MonitorUpdate
from app.services.monitor_service import MonitorService

router = APIRouter(
    prefix="/monitors",
    tags=["monitors"],
    dependencies=[Depends(get_current_user)],
)

MonitorServiceDep = Annotated[MonitorService, Depends(get_monitor_service)]


@router.get("/", response_model=list[MonitorOut])
async def list_monitors(service: MonitorServiceDep) -> list[MonitorOut]:
    return await service.list_monitors()


@router.get("/{monitor_id}", response_model=MonitorOut)
async def get_monitor(monitor_id: int, service: MonitorServiceDep) -> MonitorOut:
    monitor = await service.get_monitor(monitor_id)
    if not monitor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Monitor not found")
    return monitor


@router.post("/", response_model=MonitorOut, status_code=status.HTTP_201_CREATED)
async def create_monitor(payload: MonitorCreate, service: MonitorServiceDep) -> MonitorOut:
    monitor = await service.create_monitor(payload)
    await service.session.commit()
    return monitor


@router.put("/{monitor_id}", response_model=MonitorOut)
async def update_monitor(
    monitor_id: int, payload: MonitorUpdate, service: MonitorServiceDep
) -> MonitorOut:
    monitor = await service.update_monitor(monitor_id, payload)
    if not monitor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Monitor not found")
    await service.session.commit()
    return monitor


@router.delete("/{monitor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_monitor(monitor_id: int, service: MonitorServiceDep) -> None:
    deleted = await service.delete_monitor(monitor_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Monitor not found")
    await service.session.commit()
