from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SSLCertificateStatus:
    host: str
    expires_in_days: int
    valid: bool


class SSLService:
    async def evaluate(self, host: str) -> SSLCertificateStatus:  # pragma: no cover
        # Placeholder implementation
        return SSLCertificateStatus(host=host, expires_in_days=30, valid=True)
