from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.monitor import Monitor
from app.models.security_audit import SecurityAudit, SecurityAuditStatus
from app.services.notification_service import NotificationService
from app.services.security_check_service import SecurityCheckResult, SecurityCheckService

SECURITY_RATE_SECONDS = 60


class RateLimitExceeded(Exception):
    pass


class SecurityAuditService:
    def __init__(
        self,
        session: AsyncSession,
        notification_service: NotificationService | None = None,
    ) -> None:
        self.session = session
        self.notification_service = notification_service or NotificationService()

    async def latest_for_monitor(self, monitor_id: int) -> Optional[SecurityAudit]:
        stmt: Select[tuple[SecurityAudit]] = (
            select(SecurityAudit)
            .where(SecurityAudit.monitor_id == monitor_id)
            .order_by(SecurityAudit.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_audits(
        self, monitor_id: int, limit: int = 10, offset: int = 0
    ) -> list[SecurityAudit]:
        stmt: Select[tuple[SecurityAudit]] = (
            select(SecurityAudit)
            .where(SecurityAudit.monitor_id == monitor_id)
            .order_by(SecurityAudit.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def run_monitor_audit(
        self,
        monitor: Monitor,
        security_service: SecurityCheckService,
    ) -> SecurityAudit:
        if not self._can_run(monitor):
            raise RateLimitExceeded("Security checks limited to 60s per monitor")

        security_result = await security_service.run_passive_checks(monitor.target)
        audit = await self._persist_audit(monitor, security_result)
        await self._maybe_notify(monitor, audit)
        return audit

    def _can_run(self, monitor: Monitor) -> bool:
        if not monitor.last_security_check_at:
            return True
        return datetime.now(timezone.utc) - monitor.last_security_check_at >= timedelta(
            seconds=SECURITY_RATE_SECONDS
        )

    async def _persist_audit(
        self, monitor: Monitor, result: SecurityCheckResult
    ) -> SecurityAudit:
        status = self._derive_status(result)
        monitor.last_security_check_at = datetime.now(timezone.utc)
        monitor.security_status = status
        audit = SecurityAudit(
            monitor_id=monitor.id,
            status=status,
            findings=result.checks,
        )
        self.session.add(audit)
        await self.session.flush()
        await self.session.refresh(audit)
        return audit

    async def _maybe_notify(self, monitor: Monitor, audit: SecurityAudit) -> None:
        if audit.status == SecurityAuditStatus.PASS:
            return

        config = monitor.config or {}
        recipients = config.get("alert_emails", [])
        subject = f"Security alert for monitor {monitor.name} ({audit.status})"
        body = f"Latest security findings:\n{audit.findings}"
        if recipients:
            await self.notification_service.send_email(recipients, subject, body)

        webhooks = config.get("webhooks", [])
        payload = {
            "monitor_id": monitor.id,
            "monitor_name": monitor.name,
            "status": audit.status,
            "findings": audit.findings,
        }
        for hook in webhooks:
            await self.notification_service.send_webhook(hook, payload)

    def _derive_status(self, result: SecurityCheckResult) -> SecurityAuditStatus:
        exposure = result.checks.get("exposure_checks", {})
        if exposure.get("dot_env", {}).get("exposed") or exposure.get("git_head", {}).get("exposed"):
            return SecurityAuditStatus.CRITICAL

        ssl_info = result.checks.get("ssl_security", {})
        if not ssl_info.get("enabled") or ssl_info.get("weak_cipher"):
            return SecurityAuditStatus.WARNING

        if exposure.get("robots_disallows"):
            return SecurityAuditStatus.WARNING

        return SecurityAuditStatus.PASS
