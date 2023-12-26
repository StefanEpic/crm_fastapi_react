from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.auth.models import User
from src.apps.auth.schemas import UserLogin
from src.apps.auth.utils import authorize, create_refresh_jwt, create_access_jwt, pwd_context, error_401
from src.db.db import get_session

router = APIRouter(
    prefix="",
    tags=["Authentication"],
)


@router.post('/login')
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    # check if email exists
    stmt = select(User).where(User.email == data.email)
    user = await session.execute(stmt)
    user = user.scalar_one()
    if not user:
        raise error_401
    # check if password matches
    matches = pwd_context.verify(data.password, user.password)
    if not matches:
        raise error_401
    # create jwt tokens
    data = {'email': user.email}
    access_tkn = await create_access_jwt(data)
    refresh_tkn = await create_refresh_jwt(data)

    return {
        'email': user.email,
        'access_token': access_tkn,
        'refresh_token': refresh_tkn,
        'type': 'bearer'
    }


@router.post('/refresh_token')
async def refresh(token_data: dict = Depends(authorize)):
    return token_data
