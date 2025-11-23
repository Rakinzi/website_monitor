from __future__ import annotations

import asyncio
from typing import Awaitable, Callable


class CronWorker:
    def __init__(self, interval_seconds: int = 60) -> None:
        self.interval_seconds = interval_seconds
        self._jobs: list[Callable[[], Awaitable[None]]] = []

    def register(self, job: Callable[[], Awaitable[None]]) -> None:  # pragma: no cover
        self._jobs.append(job)

    async def run(self) -> None:  # pragma: no cover
        while True:
            for job in self._jobs:
                await job()
            await asyncio.sleep(self.interval_seconds)
