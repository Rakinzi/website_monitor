from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession


class IncidentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def log_incident(self, *_, **__) -> None:  # pragma: no cover - placeholder
        """Placeholder for real incident workflows."""
        raise NotImplementedError
