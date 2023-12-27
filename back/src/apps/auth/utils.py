import datetime
from typing import Union
from fastapi import HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config import JWT_ACCESS_TOKEN_EXP_DAYS, JWT_REFRESH_TOKEN_EXP_DAYS, JWT_ALGORITHM, JWT_SECRET_KEY
from src.apps.auth.models import User
from src.db.base_db import get_session
from src.utils.base_errors import ERROR_401

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme")
            if not await self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code")

    async def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = await decode_jwt(jwtoken)
        except JWTError:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


async def create_access_jwt(data: dict):
    data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=JWT_ACCESS_TOKEN_EXP_DAYS)
    data["mode"] = "access_token"
    return jwt.encode(data, JWT_SECRET_KEY, JWT_ALGORITHM)


async def create_refresh_jwt(data: dict):
    data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=JWT_REFRESH_TOKEN_EXP_DAYS)
    data["mode"] = "refresh_token"
    return jwt.encode(data, JWT_SECRET_KEY, JWT_ALGORITHM)


async def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= datetime.datetime.utcnow().timestamp() else None
    except JWTError:
        return {}


async def verified_user(
    token: str = Depends(JWTBearer()), session: AsyncSession = Depends(get_session)
) -> Union[User, HTTPException]:
    """
    Validate the access jwt token
    :param token:
    :param session:
    :return:
    """
    try:
        data = await decode_jwt(token)
        # check if "mode": "refresh_token"
        if "email" not in data and "mode" not in data:
            raise ERROR_401
        if data["mode"] != "access_token":
            raise ERROR_401
        # check if user exists
        stmt = select(User).where(User.email == data["email"])
        user = await session.execute(stmt)
        user = user.scalar_one()

        if not user:
            raise ERROR_401

        return user
    except JWTError:
        raise ERROR_401
