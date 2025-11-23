from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.incident import IncidentStatus


class IncidentBase(BaseModel):
    summary: str = Field(min_length=3, max_length=255)
    details: Optional[dict[str, Any]] = None


class IncidentCreate(IncidentBase):
    monitor_id: int


class IncidentUpdate(BaseModel):
    status: Optional[IncidentStatus] = None
    details: Optional[dict[str, Any]] = None


class IncidentOut(IncidentBase):
    id: int
    monitor_id: int
    status: IncidentStatus
    opened_at: datetime
    resolved_at: Optional[datetime]
    timeline: Optional[list[dict[str, Any]]]

    model_config = ConfigDict(from_attributes=True)
