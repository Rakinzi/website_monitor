from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.escalation import EscalationPolicy


class EscalationPolicyBase(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    rules: Optional[dict[str, Any]] = Field(default=None)


class EscalationPolicyCreate(EscalationPolicyBase):
    pass


class EscalationPolicyUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=128)
    rules: Optional[dict[str, Any]] = None


class EscalationPolicyOut(EscalationPolicyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
