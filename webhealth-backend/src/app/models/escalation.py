from __future__ import annotations

from sqlalchemy import Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EscalationPolicy(Base):
    __tablename__ = "escalation_policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    rules: Mapped[dict | None] = mapped_column(JSON)
