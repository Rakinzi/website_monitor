"""Application configuration helpers."""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, field_validator

load_dotenv()


class Settings(BaseModel):
    """Lightweight settings object using environment variables."""

    app_name: str = "WebHealth"
    api_prefix: str = "/api"
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/webhealth",
    )
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE", "30"))
    refresh_token_expire_minutes: int = int(
        os.getenv("REFRESH_TOKEN_EXPIRE", str(60 * 24 * 7))
    )
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-me")
    jwt_refresh_secret_key: str = os.getenv("JWT_REFRESH_SECRET_KEY", "change-me-refresh")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    email_from: Optional[str] = os.getenv("EMAIL_FROM")
    webhook_timeout_seconds: int = int(os.getenv("WEBHOOK_TIMEOUT", "5"))
    mail_server: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    mail_port: int = int(os.getenv("MAIL_PORT", "587"))
    mail_use_tls: bool = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    mail_username: Optional[str] = os.getenv("MAIL_USERNAME", "leightonsilver@gmail.com")
    mail_password: Optional[str] = os.getenv("MAIL_PASSWORD", "qxfjyciwtityhvrz")
    mail_default_sender: Optional[str] = os.getenv("MAIL_DEFAULT_SENDER", "silverrakinzi@gmail.com")

    @field_validator("database_url")
    @classmethod
    def _ensure_async_driver(cls, value: str) -> str:
        if "+asyncpg" not in value and value.startswith("postgresql"):
            return value.replace("postgresql", "postgresql+asyncpg")
        return value

    @field_validator("app_name")
    @classmethod
    def _validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("app_name must not be empty")
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
