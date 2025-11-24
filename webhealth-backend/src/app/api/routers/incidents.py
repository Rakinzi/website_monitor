from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_incident_service
from app.schemas.incident_schemas import IncidentOut
from app.services.incident_service import IncidentService

router = APIRouter(prefix="/incidents", tags=["incidents"])


IncidentServiceDep = Annotated[IncidentService, Depends(get_incident_service)]


@router.get("/", response_model=List[IncidentOut])
async def list_incidents(
    service: IncidentServiceDep,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> List[IncidentOut]:
    return await service.list_incidents(limit=limit, offset=offset)
