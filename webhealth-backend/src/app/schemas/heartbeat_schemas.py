from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HeartbeatOut(BaseModel):
    id: int
    monitor_id: int
    token: str
    last_ping_at: datetime | None
    status: str

    model_config = ConfigDict(from_attributes=True)
