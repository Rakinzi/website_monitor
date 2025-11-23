from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.region import Region
from app.schemas.region_schemas import RegionCreate


class RegionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_regions(self) -> list[Region]:
        result = await self.session.execute(select(Region))
        return list(result.scalars())

    async def create_region(self, payload: RegionCreate) -> Region:
        region = Region(**payload.model_dump())
        self.session.add(region)
        await self.session.flush()
        await self.session.refresh(region)
        return region
