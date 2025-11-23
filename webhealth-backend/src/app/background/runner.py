from __future__ import annotations

import asyncio
from typing import Awaitable, Callable

TaskFactory = Callable[[], Awaitable[None]]


class BackgroundRunner:
    def __init__(self) -> None:
        self._tasks: list[asyncio.Task] = []

    def add(self, factory: TaskFactory) -> None:  # pragma: no cover - placeholder
        self._tasks.append(asyncio.create_task(factory()))
