from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class RegionCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    code: str = Field(min_length=2, max_length=16)
    provider: str = Field(default="global")


class RegionOut(RegionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
