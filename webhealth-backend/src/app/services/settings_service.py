from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.settings import AppSettings
from app.models.escalation import EscalationPolicy
from app.schemas.settings_schemas import SettingsUpdate
from app.schemas.escalation_schemas import EscalationPolicyCreate, EscalationPolicyUpdate


class SettingsService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_settings(self) -> AppSettings:
        settings = await self.session.get(AppSettings, 1)
        if not settings:
            settings = AppSettings(id=1)
            self.session.add(settings)
            await self.session.commit()
            await self.session.refresh(settings)
        return settings

    async def update_settings(self, payload: SettingsUpdate) -> AppSettings:
        settings = await self.get_settings()
        data = payload.model_dump()
        # map camelCase to snake_case manual
        settings.email_notifications = data["emailNotifications"]
        settings.slack_notifications = data["slackNotifications"]
        settings.push_notifications = data["pushNotifications"]
        settings.webhook_url = str(data["webhookUrl"]) if data["webhookUrl"] else None
        settings.email_address = data["emailAddress"]
        settings.check_interval = data["checkInterval"]
        settings.retry_attempts = data["retryAttempts"]
        settings.timeout_seconds = data["timeout"]
        settings.ssl_verification = data["sslVerification"]
        settings.follow_redirects = data["followRedirects"]
        await self.session.commit()
        await self.session.refresh(settings)
        return settings

    async def list_escalations(self) -> list[EscalationPolicy]:
        stmt = select(EscalationPolicy).order_by(EscalationPolicy.id.asc())
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def create_escalation(self, payload: EscalationPolicyCreate) -> EscalationPolicy:
        policy = EscalationPolicy(**payload.model_dump())
        self.session.add(policy)
        await self.session.flush()
        await self.session.refresh(policy)
        await self.session.commit()
        return policy

    async def update_escalation(self, policy_id: int, payload: EscalationPolicyUpdate) -> EscalationPolicy | None:
        policy = await self.session.get(EscalationPolicy, policy_id)
        if not policy:
            return None
        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(policy, key, value)
        await self.session.commit()
        await self.session.refresh(policy)
        return policy

    async def delete_escalation(self, policy_id: int) -> bool:
        policy = await self.session.get(EscalationPolicy, policy_id)
        if not policy:
            return False
        await self.session.delete(policy)
        await self.session.commit()
        return True
