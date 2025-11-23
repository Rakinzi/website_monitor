from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SecurityAuditStatus(str, enum.Enum):
    PASS = "pass"
    WARNING = "warning"
    CRITICAL = "critical"


class SecurityAudit(Base):
    __tablename__ = "security_audits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    monitor_id: Mapped[int] = mapped_column(ForeignKey("monitors.id"), nullable=False)
    status: Mapped[SecurityAuditStatus] = mapped_column(
        Enum(SecurityAuditStatus), default=SecurityAuditStatus.PASS, nullable=False
    )
    findings: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    monitor: Mapped["Monitor"] = relationship("Monitor", back_populates="security_audits")


if TYPE_CHECKING:  # pragma: no cover - typing hints only
    from app.models.monitor import Monitor
