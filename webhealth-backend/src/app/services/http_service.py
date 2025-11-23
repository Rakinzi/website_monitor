from __future__ import annotations

import httpx


class HttpService:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=10)

    async def get(self, url: str, **kwargs):  # pragma: no cover - placeholder
        return await self._client.get(url, **kwargs)
