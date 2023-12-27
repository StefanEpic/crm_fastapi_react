import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr

from src.apps.auth.models import UserPermission


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    registration_date: datetime.datetime
    permission: UserPermission


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class ReturnTokenSchema(BaseModel):
    email: EmailStr
    access_token: str
    refresh_token: str
    token_type: str
