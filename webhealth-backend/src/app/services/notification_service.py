from __future__ import annotations

import asyncio
import smtplib
from email.message import EmailMessage
from typing import Iterable

import httpx

from app.core.config import settings


class NotificationService:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=settings.webhook_timeout_seconds)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def send_email(self, recipients: Iterable[str], subject: str, body: str) -> None:
        recipient_list = [r for r in recipients if r]
        if not recipient_list or not settings.mail_server:
            return
        await asyncio.to_thread(self._send_email_sync, recipient_list, subject, body)

    def _send_email_sync(self, recipients: list[str], subject: str, body: str) -> None:
        msg = EmailMessage()
        msg["Subject"] = subject
        sender = settings.mail_default_sender or settings.mail_username
        if not sender:
            return
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg.set_content(body)

        with smtplib.SMTP(settings.mail_server, settings.mail_port, timeout=20) as server:
            if settings.mail_use_tls:
                server.starttls()
            if settings.mail_username and settings.mail_password:
                server.login(settings.mail_username, settings.mail_password)
            server.send_message(msg)

    async def send_webhook(self, url: str, payload: dict) -> httpx.Response:
        return await self._client.post(url, json=payload)
