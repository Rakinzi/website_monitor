from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel, HttpUrl


class SecurityCheckRequest(BaseModel):
    url: HttpUrl


class SecurityCheckResponse(BaseModel):
    url: HttpUrl
    checks: Dict[str, Any]
