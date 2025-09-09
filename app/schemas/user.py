from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSignupRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: Optional[str] = None


class UserSignupResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: Optional[str] = None
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
