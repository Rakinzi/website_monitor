from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.monitor import MonitorStatus, MonitorType
from app.models.security_audit import SecurityAuditStatus


class MonitorBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    monitor_type: MonitorType = MonitorType.HTTP
    target: str = Field(min_length=1, max_length=2048)
    interval_seconds: int = Field(default=60, ge=15, le=3600)
    timeout_seconds: int = Field(default=5, ge=1, le=60)
    threshold_latency_ms: Optional[int] = Field(default=1000, ge=1, le=60000)
    failure_threshold: int = Field(default=3, ge=1, le=10)
    success_threshold: int = Field(default=1, ge=1, le=10)
    regions: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    config: dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True


class MonitorCreate(MonitorBase):
    pass


class MonitorUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    monitor_type: Optional[MonitorType] = None
    target: Optional[str] = Field(default=None, min_length=1, max_length=2048)
    interval_seconds: Optional[int] = Field(default=None, ge=15, le=3600)
    timeout_seconds: Optional[int] = Field(default=None, ge=1, le=60)
    threshold_latency_ms: Optional[int] = Field(default=None, ge=1, le=60000)
    failure_threshold: Optional[int] = Field(default=None, ge=1, le=10)
    success_threshold: Optional[int] = Field(default=None, ge=1, le=10)
    regions: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    config: Optional[dict[str, Any]] = None
    is_active: Optional[bool] = None
    status: Optional[MonitorStatus] = None


class MonitorOut(MonitorBase):
    id: int
    status: MonitorStatus
    created_at: datetime
    updated_at: datetime
    security_status: SecurityAuditStatus
    last_security_check_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
