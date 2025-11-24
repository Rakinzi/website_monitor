from __future__ import annotations

import asyncio

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.monitor import Monitor, MonitorStatus, MonitorType
from app.models.user import UserRole
from app.schemas.user_schemas import UserCreate
from app.services.monitor_service import MonitorService
from app.services.user_service import UserService

ADMIN_EMAIL = "admin@webhealth.dev"
ADMIN_PASSWORD = "ChangeMe123!"

MONITORS = [
    {
        "name": "Production API",
        "description": "Primary API uptime",
        "monitor_type": MonitorType.HTTP,
        "target": "https://api.example.com/health",
        "interval_seconds": 60,
        "timeout_seconds": 5,
        "regions": ["us-east-1", "eu-west-1"],
        "tags": ["production", "api"],
        "config": {
            "alert_emails": ["alerts@example.com"],
            "webhooks": [],
        },
    },
    {
        "name": "Global CDN",
        "description": "CDN SSL + latency",
        "monitor_type": MonitorType.SSL,
        "target": "https://cdn.example.com",
        "interval_seconds": 300,
        "timeout_seconds": 10,
        "regions": ["us", "eu", "apac"],
        "tags": ["cdn"],
        "config": {},
    },
]


async def seed_admin_user(session) -> None:
    user_service = UserService(session)
    existing = await user_service.get_by_email(ADMIN_EMAIL)
    if existing:
        print(f"Admin user already exists: {ADMIN_EMAIL}")
        return

    admin = await user_service.create_user(
        UserCreate(email=ADMIN_EMAIL, password=ADMIN_PASSWORD, role=UserRole.ADMIN)
    )
    session.add(admin)
    await session.commit()
    print(f"Created admin user {ADMIN_EMAIL} with password {ADMIN_PASSWORD}")


async def seed_monitors(session) -> None:
    for payload in MONITORS:
        result = await session.execute(
            select(Monitor).where(Monitor.name == payload["name"])
        )
        if result.scalar_one_or_none():
            print(f"Monitor {payload['name']} already exists")
            continue
        monitor = Monitor(**payload, status=MonitorStatus.UNKNOWN)
        session.add(monitor)
        await session.flush()
        print(f"Created monitor {monitor.name}")
    await session.commit()


async def main() -> None:
    async with AsyncSessionLocal() as session:
        await seed_admin_user(session)
        await seed_monitors(session)


if __name__ == "__main__":
    asyncio.run(main())
