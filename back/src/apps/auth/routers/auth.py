from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.auth.repositories import AuthRepository
from src.apps.auth.schemas import UserCreate, ReturnTokenSchema, RefreshTokenSchema
from src.db.base_db import get_session

router = APIRouter(
    prefix="",
    tags=["Authentication"],
)


@router.post(
    "/access",
    response_model=ReturnTokenSchema,
    summary="Get new access and refresh tokens",
    description="Post email and password for get access and refresh tokens",
)
async def get_access_token(user: UserCreate, session: AsyncSession = Depends(get_session)) -> ReturnTokenSchema:
    return await AuthRepository(session).get_access_token(user)


@router.post(
    "/refresh",
    response_model=ReturnTokenSchema,
    summary="Update access and refresh tokens",
    description="Post refresh token for get a new access and refresh tokens",
)
async def get_refresh_token(
    token: RefreshTokenSchema, session: AsyncSession = Depends(get_session)
) -> ReturnTokenSchema:
    return await AuthRepository(session).get_refresh_token(token)
