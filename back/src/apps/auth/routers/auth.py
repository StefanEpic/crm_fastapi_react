from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.auth.models import User
from src.apps.auth.schemas import Token, UserLogin
from src.apps.auth.utils import verified_user, authorize, create_refresh_jwt, \
    create_access_jwt, pwd_context
from src.db.db import get_session

router = APIRouter(
    prefix="",
    tags=["Authentication"],
)


@router.post('/login')
async def login(body: UserLogin, session: AsyncSession = Depends(get_session)):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='wrong credentials'
    )
    # check if email exists
    user = await session.get(User, body.email)
    if not user:
        raise error
    # check if password matches
    matches = pwd_context.verify(body.password, user.password_hash)
    if not matches:
        raise error
    # create jwt access token
    data = {'user_name': user.email}
    access_tkn = create_access_jwt(data)
    # create jwt refresh token
    refresh_tkn = create_refresh_jwt(data)
    # store the refresh token in memory||database|| any storage
    # in my case I am storing in users-table
    await session.get(User, body.email).update(**{'refresh_token': refresh_tkn})

    return {
        'email': user.email,
        'access_token': access_tkn,
        'refresh_token': refresh_tkn,
        'type': 'bearer'
    }


@router.post('/refresh_token')
async def refresh(token_data: dict = Depends(authorize)):
    return token_data


@router.get('/me')
async def protected_data(user: User = Depends(verified_user)):
    return {'status': 'authorized', 'email': user.email}
