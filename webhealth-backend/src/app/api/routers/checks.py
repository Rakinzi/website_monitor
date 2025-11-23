from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import (
    get_monitor_service,
    get_security_audit_service,
    get_security_check_service,
)
from app.schemas.security_audit_schemas import SecurityAuditOut
from app.schemas.security_schemas import SecurityCheckRequest, SecurityCheckResponse
from app.services.monitor_service import MonitorService
from app.services.security_audit_service import RateLimitExceeded, SecurityAuditService
from app.services.security_check_service import SecurityCheckService

router = APIRouter(prefix="/checks", tags=["checks"])

SecurityCheckDep = Annotated[SecurityCheckService, Depends(get_security_check_service)]
SecurityAuditDep = Annotated[SecurityAuditService, Depends(get_security_audit_service)]
MonitorServiceDep = Annotated[MonitorService, Depends(get_monitor_service)]


@router.post("/security", response_model=SecurityCheckResponse)
async def run_security_checks(
    payload: SecurityCheckRequest,
    service: SecurityCheckDep,
) -> SecurityCheckResponse:
    result = await service.run_passive_checks(str(payload.url))
    return SecurityCheckResponse(url=payload.url, checks=result.checks)


@router.post(
    "/security/monitors/{monitor_id}",
    response_model=SecurityAuditOut,
    status_code=status.HTTP_201_CREATED,
)
async def run_monitor_security_check(
    monitor_id: int,
    monitor_service: MonitorServiceDep,
    audit_service: SecurityAuditDep,
    security_service: SecurityCheckDep,
) -> SecurityAuditOut:
    monitor = await monitor_service.get_monitor(monitor_id)
    if not monitor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Monitor not found")
    try:
        audit = await audit_service.run_monitor_audit(monitor, security_service)
        await audit_service.session.commit()
        return audit
    except RateLimitExceeded as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        ) from exc


@router.get("/security/monitors/{monitor_id}/latest", response_model=SecurityAuditOut)
async def get_latest_security_audit(
    monitor_id: int,
    audit_service: SecurityAuditDep,
) -> SecurityAuditOut:
    audit = await audit_service.latest_for_monitor(monitor_id)
    if not audit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No audits found")
    return audit


@router.get(
    "/security/monitors/{monitor_id}/audits",
    response_model=list[SecurityAuditOut],
)
async def list_security_audits(
    monitor_id: int,
    audit_service: SecurityAuditDep,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> list[SecurityAuditOut]:
    return await audit_service.list_audits(monitor_id, limit=limit, offset=offset)
