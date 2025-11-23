from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Enum, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.security_audit import SecurityAuditStatus


class MonitorType(str, enum.Enum):
    HTTP = "http"
    REGIONAL = "regional"
    SYNTHETIC = "synthetic"
    SSL = "ssl"
    HEARTBEAT = "heartbeat"


class MonitorStatus(str, enum.Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"
    UNKNOWN = "unknown"


class Monitor(Base):
    __tablename__ = "monitors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text())
    monitor_type: Mapped[MonitorType] = mapped_column(
        Enum(MonitorType), default=MonitorType.HTTP, nullable=False
    )
    target: Mapped[str] = mapped_column(String(2048), nullable=False)
    interval_seconds: Mapped[int] = mapped_column(Integer, default=60)
    timeout_seconds: Mapped[int] = mapped_column(Integer, default=5)
    threshold_latency_ms: Mapped[Optional[int]] = mapped_column(Integer)
    failure_threshold: Mapped[int] = mapped_column(Integer, default=3)
    success_threshold: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[MonitorStatus] = mapped_column(
        Enum(MonitorStatus), default=MonitorStatus.UNKNOWN, nullable=False
    )
    regions: Mapped[Optional[list[str]]] = mapped_column(JSON)
    tags: Mapped[Optional[list[str]]] = mapped_column(JSON)
    config: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    last_security_check_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    security_status: Mapped[SecurityAuditStatus] = mapped_column(
        Enum(SecurityAuditStatus), default=SecurityAuditStatus.PASS, nullable=False
    )

    checks: Mapped[list["CheckLog"]] = relationship(
        "CheckLog", back_populates="monitor", cascade="all, delete-orphan"
    )
    incidents: Mapped[list["Incident"]] = relationship(
        "Incident", back_populates="monitor", cascade="all, delete-orphan"
    )
    security_audits: Mapped[list["SecurityAudit"]] = relationship(
        "SecurityAudit", back_populates="monitor", cascade="all, delete-orphan"
    )


if TYPE_CHECKING:  # pragma: no cover - typing only
    from app.models.check import CheckLog
    from app.models.incident import Incident
    from app.models.security_audit import SecurityAudit
