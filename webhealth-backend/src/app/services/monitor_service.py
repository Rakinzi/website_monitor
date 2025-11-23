from __future__ import annotations

from datetime import datetime

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.monitor import Monitor, MonitorStatus
from app.schemas.monitor_schemas import MonitorCreate, MonitorUpdate


class MonitorService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_monitors(self) -> list[Monitor]:
        statement: Select[tuple[Monitor]] = select(Monitor).order_by(Monitor.created_at.desc())
        result = await self.session.execute(statement)
        return list(result.scalars())

    async def get_monitor(self, monitor_id: int) -> Monitor | None:
        return await self.session.get(Monitor, monitor_id)

    async def create_monitor(self, payload: MonitorCreate) -> Monitor:
        monitor = Monitor(**payload.model_dump())
        self.session.add(monitor)
        await self.session.flush()
        await self.session.refresh(monitor)
        return monitor

    async def update_monitor(self, monitor_id: int, payload: MonitorUpdate) -> Monitor | None:
        monitor = await self.get_monitor(monitor_id)
        if not monitor:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(monitor, key, value)
        monitor.updated_at = datetime.utcnow()
        await self.session.flush()
        await self.session.refresh(monitor)
        return monitor

    async def delete_monitor(self, monitor_id: int) -> bool:
        monitor = await self.get_monitor(monitor_id)
        if not monitor:
            return False
        await self.session.delete(monitor)
        return True

    async def mark_status(self, monitor_id: int, status: MonitorStatus) -> Monitor | None:
        monitor = await self.get_monitor(monitor_id)
        if not monitor:
            return None
        monitor.status = status
        monitor.updated_at = datetime.utcnow()
        await self.session.flush()
        await self.session.refresh(monitor)
        return monitor
