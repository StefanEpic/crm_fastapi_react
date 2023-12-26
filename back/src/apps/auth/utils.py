import datetime
from typing import Union
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import JWT_ACCESS_TOKEN_EXP_DAYS, JWT_REFRESH_TOKEN_EXP_DAYS, JWT_ALGORITHM, JWT_SECRET_KEY
from src.apps.auth.models import User
from src.db.db import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
error_401 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid authorization credentials'
)


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)


async def create_access_jwt(data: dict):
    data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=JWT_ACCESS_TOKEN_EXP_DAYS)
    data['mode'] = 'access_token'
    return jwt.encode(data, JWT_SECRET_KEY, JWT_ALGORITHM)


async def create_refresh_jwt(data: dict):
    data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=JWT_REFRESH_TOKEN_EXP_DAYS)
    data['mode'] = 'refresh_token'
    return jwt.encode(data, JWT_SECRET_KEY, JWT_ALGORITHM)


async def authorize(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> dict:
    """
    Validate the refresh jwt token
    :param token:
    :param session:
    :return:
    """
    try:
        data = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
        # check if "mode": "refresh_token"
        if 'email' not in data and 'mode' not in data:
            raise error_401
        if data['mode'] != 'refresh_token':
            raise error_401
        # check if user exists
        stmt = select(User).where(User.email == data['email'])
        user = await session.execute(stmt)
        user = user.scalar_one()
        if not user:
            raise error_401
        # generate new tokens
        data = {'email': user.email}
        access_tkn = create_access_jwt(data)
        refresh_tkn = create_refresh_jwt(data)
        return {
            'access_token': access_tkn,
            'refresh_token': refresh_tkn,
            'type': 'bearer'
        }
    except JWTError:
        raise error_401


async def verified_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session)
) -> Union[User, HTTPException]:
    """
    Validate the access jwt token
    :param token:
    :param session:
    :return:
    """
    try:
        data = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
        # check if "mode": "refresh_token"
        if 'email' not in data and 'mode' not in data:
            raise error_401
        if data['mode'] != 'access_token':
            raise error_401
        # check if user exists
        stmt = select(User).where(User.email == data['email'])
        user = await session.execute(stmt)
        user = user.scalar_one()
        if not user:
            raise error_401

        return user
    except JWTError:
        raise error_401
