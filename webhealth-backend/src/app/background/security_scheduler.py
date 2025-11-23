from __future__ import annotations

import asyncio
import contextlib

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models.monitor import Monitor
from app.services.notification_service import NotificationService
from app.services.security_audit_service import RateLimitExceeded, SecurityAuditService
from app.services.security_check_service import SecurityCheckService


class SecurityAuditScheduler:
    """Background worker that runs passive security checks on active monitors."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        interval_seconds: int = 300,
    ) -> None:
        self.session_factory = session_factory
        self.interval_seconds = interval_seconds
        self._task: asyncio.Task | None = None
        self._stopped = asyncio.Event()

    async def start(self) -> None:
        if self._task and not self._task.done():
            return
        self._stopped.clear()
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self) -> None:
        if not self._task:
            return
        self._stopped.set()
        self._task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._task
        self._task = None

    async def _run_loop(self) -> None:
        try:
            while not self._stopped.is_set():
                await self._run_once()
                try:
                    await asyncio.wait_for(
                        self._stopped.wait(), timeout=self.interval_seconds
                    )
                except asyncio.TimeoutError:
                    continue
        except asyncio.CancelledError:
            pass

    async def _run_once(self) -> None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(Monitor).where(Monitor.is_active.is_(True))
            )
            monitors = result.scalars().all()
            if not monitors:
                return

            security_service = SecurityCheckService()
            notification_service = NotificationService()
            audit_service = SecurityAuditService(session, notification_service)
            try:
                for monitor in monitors:
                    try:
                        await audit_service.run_monitor_audit(monitor, security_service)
                    except RateLimitExceeded:
                        continue
                await session.commit()
            finally:
                await security_service.aclose()
                await notification_service.aclose()
