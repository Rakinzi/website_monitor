from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict

from app.models.security_audit import SecurityAuditStatus


class SecurityAuditOut(BaseModel):
    id: int
    monitor_id: int
    status: SecurityAuditStatus
    findings: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
