from __future__ import annotations

from typing import Any


class SyntheticService:
    async def run_journey(self, script: dict[str, Any]):  # pragma: no cover - placeholder
        return {"status": "ok", "steps": len(script.get("steps", []))}
