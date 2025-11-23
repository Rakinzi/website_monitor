from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db_session, get_user_service
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.models.user import User
from app.schemas.auth_schemas import (
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
    TokenPair,
)
from app.schemas.user_schemas import UserCreate, UserOut
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate,
    user_service: UserServiceDep,
    session: SessionDep,
) -> UserOut:
    existing = await user_service.get_by_email(payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that email already exists",
        )
    user = await user_service.create_user(payload)
    await session.commit()
    return user


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, user_service: UserServiceDep) -> LoginResponse:
    user = await user_service.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user,
    )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(payload: RefreshRequest) -> RefreshResponse:
    try:
        token_data = decode_token(payload.refresh_token, refresh=True)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        ) from exc

    user_id = token_data.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    return RefreshResponse(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserOut)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]) -> UserOut:
    return current_user


@router.post("/logout", response_model=TokenPair)
async def logout() -> TokenPair:
    return TokenPair(access_token="", refresh_token="")
