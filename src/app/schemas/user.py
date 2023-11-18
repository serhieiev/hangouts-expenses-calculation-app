import re
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from uuid import UUID
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    avatar: Optional[str]

    @validator("password")
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.search(r"[0-9]", password):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character")

        return password


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    avatar: Optional[str]
    created_at: datetime
    modified_at: datetime


class UserInDB(BaseModel):
    id: UUID
    email: EmailStr
    avatar: Optional[str]
    created_at: datetime
    modified_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
