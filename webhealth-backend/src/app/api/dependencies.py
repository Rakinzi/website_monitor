from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_session
from app.models.user import User
from app.services.monitor_service import MonitorService
from app.services.notification_service import NotificationService
from app.services.incident_service import IncidentService
from app.services.security_audit_service import SecurityAuditService
from app.services.security_check_service import SecurityCheckService
from app.services.user_service import UserService
from app.services.settings_service import SettingsService


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async for session in get_session():
        yield session


def get_monitor_service(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> MonitorService:
    return MonitorService(session)


def get_incident_service(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> IncidentService:
    return IncidentService(session)


def get_user_service(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> UserService:
    return UserService(session)


async def get_security_check_service() -> AsyncIterator[SecurityCheckService]:
    service = SecurityCheckService()
    try:
        yield service
    finally:
        await service.aclose()


async def get_notification_service() -> AsyncIterator[NotificationService]:
    service = NotificationService()
    try:
        yield service
    finally:
        await service.aclose()


def get_security_audit_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    notification_service: Annotated[
        NotificationService, Depends(get_notification_service)
    ],
) -> SecurityAuditService:
    return SecurityAuditService(session, notification_service)


def get_settings_service(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> SettingsService:
    return SettingsService(session)


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    credentials: Annotated[
        Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)
    ],
) -> User:
    token = credentials.credentials if credentials else None
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_token(token)
    except jwt.PyJWTError as exc:  # pragma: no cover - defensive
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    user = await session.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
