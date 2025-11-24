from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, EmailStr


class SettingsBase(BaseModel):
    emailNotifications: bool = Field(default=False)
    slackNotifications: bool = Field(default=False)
    pushNotifications: bool = Field(default=False)
    webhookUrl: Optional[HttpUrl] = None
    emailAddress: Optional[EmailStr] = None
    checkInterval: int = Field(default=60, ge=10, le=3600)
    retryAttempts: int = Field(default=3, ge=1, le=10)
    timeout: int = Field(default=30, ge=5, le=120)
    sslVerification: bool = Field(default=True)
    followRedirects: bool = Field(default=True)


class SettingsUpdate(SettingsBase):
    pass


class SettingsOut(SettingsBase):
    updatedAt: datetime

    model_config = ConfigDict(from_attributes=True)
