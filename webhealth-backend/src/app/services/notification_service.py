from __future__ import annotations

import asyncio
from typing import Iterable

import httpx

from app.core.config import settings


class NotificationService:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=settings.webhook_timeout_seconds)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def send_email(self, recipients: Iterable[str], subject: str, body: str) -> None:
        # Placeholder: integrate with SES, SendGrid, etc.
        if not recipients:
            return
        await asyncio.sleep(0)

    async def send_webhook(self, url: str, payload: dict) -> httpx.Response:
        return await self._client.post(url, json=payload)
