from __future__ import annotations

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incident import Incident


class IncidentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_incidents(self, limit: int = 50, offset: int = 0) -> list[Incident]:
        stmt: Select[tuple[Incident]] = (
            select(Incident)
            .order_by(Incident.opened_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def log_incident(self, *_, **__) -> None:  # pragma: no cover - placeholder
        """Placeholder for real incident workflows."""
        raise NotImplementedError
