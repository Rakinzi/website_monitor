from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import (
    analytics,
    auth,
    checks,
    heartbeats,
    incidents,
    monitors,
    regions,
    webhooks,
)
from app.api.routers import settings as settings_router
from app.background.security_scheduler import SecurityAuditScheduler
from app.core.config import settings
from app.db.session import AsyncSessionLocal

security_scheduler = SecurityAuditScheduler(AsyncSessionLocal, interval_seconds=300)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await security_scheduler.start()
    try:
        yield
    finally:
        await security_scheduler.stop()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = settings.api_prefix
app.include_router(auth.router, prefix=api_prefix)
app.include_router(monitors.router, prefix=api_prefix)
app.include_router(checks.router, prefix=api_prefix)
app.include_router(incidents.router, prefix=api_prefix)
app.include_router(regions.router, prefix=api_prefix)
app.include_router(analytics.router, prefix=api_prefix)
app.include_router(heartbeats.router, prefix=api_prefix)
app.include_router(webhooks.router, prefix=api_prefix)
app.include_router(settings_router.router, prefix=api_prefix)


@app.get("/healthz")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
