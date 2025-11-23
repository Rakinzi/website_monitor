"""Async SQLAlchemy session factory."""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


def _build_engine() -> AsyncEngine:
    return create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)


engine = _build_engine()
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
