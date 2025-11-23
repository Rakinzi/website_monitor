"""SQLAlchemy declarative base and model imports."""
from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models for Alembic metadata
from app.models import monitor  # noqa: E402,F401
from app.models import check  # noqa: E402,F401
from app.models import incident  # noqa: E402,F401
from app.models import region  # noqa: E402,F401
from app.models import heartbeat  # noqa: E402,F401
from app.models import escalation  # noqa: E402,F401
from app.models import user  # noqa: E402,F401
from app.models import security_audit  # noqa: E402,F401
