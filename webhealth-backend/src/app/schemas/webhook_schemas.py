from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class WebhookCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    url: HttpUrl
    secret: str | None = None
    enabled: bool = True


class WebhookOut(WebhookCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
