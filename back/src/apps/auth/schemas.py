import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr

from src.apps.auth.models import UserPermission


class UserCreate(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    is_active: bool
    registration_date: datetime.datetime
    permission: UserPermission


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
