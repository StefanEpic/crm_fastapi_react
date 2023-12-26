import datetime
from typing import Optional, Union, Dict
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import JWT_ACCESS_TOKEN_EXP_DAYS, JWT_REFRESH_TOKEN_EXP_DAYS, JWT_ALGORITHM, JWT_SECRET_KEY
from src.apps.auth.models import User
from src.db.db import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='invalid authorization credentials'
)


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)

#
# async def get_user_by_email(email: str, session: AsyncSession) -> User:
#     stmt = select(User).where(User.email == email)
#     res = await session.execute(stmt)
#     res = res.scalar_one_or_none()
#     if not res:
#         raise HTTPException(status_code=404, detail="Not found")
#     return res
#
#
# async def authenticate_user(email: str, password: str, session: AsyncSession) -> Union[User, bool]:
#     user = await get_user_by_email(email, session)
#     if not user:
#         return False
#     if not Hasher.verify_password(password, user.password):
#         return False
#     return user
#
#
# async def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> jwt:
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# async def login_for_access_token(
#         form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)
# ) -> Dict:
#     user = await authenticate_user(form_data.username, form_data.password, session)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     refresh_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     refresh_token = await create_access_token(
#         data={"sub": user.email},
#         expires_delta=access_token_expires,
#     )
#     access_token = await create_access_token(
#         data={"sub": user.email},
#         expires_delta=access_token_expires,
#     )
#     return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
#     credentials_exception = HTTPException(status_code=200, detail="Could not validate credentials")
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = await get_user_by_email(email, session)
#     if user is None:
#         raise credentials_exception
#     return user


def create_access_jwt(data: dict):
    data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=JWT_ACCESS_TOKEN_EXP_DAYS)
    data['mode'] = 'access_token'
    return jwt.encode(data, JWT_SECRET_KEY, JWT_ALGORITHM)


def create_refresh_jwt(data: dict):
    data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=JWT_REFRESH_TOKEN_EXP_DAYS)
    data['mode'] = 'refresh_token'
    return jwt.encode(data, JWT_SECRET_KEY, JWT_ALGORITHM)


async def authorize(token: str = Depends(oauth2_scheme)) -> dict:
    # validate the refresh jwt token
    try:
        data = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
        # check if "mode": "refresh_token"
        if 'user_name' not in data and 'mode' not in data:
            raise error
        if data['mode'] != 'refresh_token':
            raise error
        # check if user exists
        user = await User.filter(email=data['user_name']).first()
        if not user or token != user.refresh_token:
            raise error
        # generate new refresh token and update user
        data = {'user_name': user.email}
        refresh_tkn = create_refresh_jwt(data)
        await User.filter(email=user.email).update(**{'refresh_token': refresh_tkn})
        # generate new access token
        access_tkn = create_access_jwt(data)
        return {
            'access_token': access_tkn,
            'refresh_token': refresh_tkn,
            'type': 'bearer'
        }
    except JWTError:
        raise error


async def verified_user(token: str = Depends(oauth2_scheme)) -> User:
    # validate the access jwt token
    try:
        data = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
        # check if "mode": "refresh_token"
        if 'user_name' not in data and 'mode' not in data:
            raise error
        if data['mode'] != 'access_token':
            raise error
        # check if user exists
        user = await User.filter(email=data['user_name']).first()
        if not user:
            raise error

        return user
    except JWTError:
        raise error
