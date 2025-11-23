from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field

from app.schemas.user_schemas import UserOut


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginResponse(TokenPair):
    user: UserOut


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(TokenPair):
    pass
