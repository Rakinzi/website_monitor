from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

import enum
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CheckType(str, enum.Enum):
    HTTP = "http"
    SSL = "ssl"
    SYNTHETIC = "synthetic"
    REGION = "region"
    HEARTBEAT = "heartbeat"


class CheckStatus(str, enum.Enum):
    PASSED = "passed"
    FAILED = "failed"
    DEGRADED = "degraded"


class CheckLog(Base):
    __tablename__ = "check_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    monitor_id: Mapped[int] = mapped_column(ForeignKey("monitors.id"), nullable=False)
    check_type: Mapped[CheckType]
    status: Mapped[CheckStatus]
    details: Mapped[Optional[dict]] = mapped_column(JSON)
    response_ms: Mapped[Optional[int]]
    region: Mapped[Optional[str]] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    duration: Mapped[Optional[int]] = mapped_column(Integer)

    monitor: Mapped["Monitor"] = relationship(back_populates="checks")


if TYPE_CHECKING:  # pragma: no cover - typing only
    from app.models.monitor import Monitor
