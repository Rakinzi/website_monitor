from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.models.check import CheckStatus, CheckType


class CheckLogOut(BaseModel):
    id: int
    monitor_id: int
    check_type: CheckType
    status: CheckStatus
    region: Optional[str]
    response_ms: Optional[int]
    details: Optional[dict[str, Any]]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
