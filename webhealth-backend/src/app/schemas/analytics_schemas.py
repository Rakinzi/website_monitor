from __future__ import annotations

from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class UptimeReport(BaseModel):
    monitor_id: int
    uptime_percentage: float
    window_start: datetime
    window_end: datetime
    breakdown: Dict[str, float]
