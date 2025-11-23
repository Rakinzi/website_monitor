from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession


class IncidentEvaluator:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def evaluate(self) -> None:  # pragma: no cover - placeholder
        pass
