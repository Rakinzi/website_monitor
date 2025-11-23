"""Security helpers for hashing secrets and issuing JWTs."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def _create_token(data: Dict[str, Any], expires_delta: timedelta, secret: str) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def create_access_token(subject: str | int, scopes: list[str] | None = None) -> str:
    payload = {"sub": str(subject), "scopes": scopes or []}
    expire_delta = timedelta(minutes=settings.access_token_expire_minutes)
    return _create_token(payload, expire_delta, settings.jwt_secret_key)


def create_refresh_token(subject: str | int) -> str:
    payload = {"sub": str(subject), "type": "refresh"}
    expire_delta = timedelta(minutes=settings.refresh_token_expire_minutes)
    return _create_token(payload, expire_delta, settings.jwt_refresh_secret_key)


def decode_token(token: str, refresh: bool = False) -> Dict[str, Any]:
    secret = settings.jwt_refresh_secret_key if refresh else settings.jwt_secret_key
    return jwt.decode(token, secret, algorithms=[settings.jwt_algorithm])
