import uuid
from typing import List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.auth.models import User
from src.apps.auth.permissions import check_permission_user, check_permission_moderator
from src.apps.auth.repositories import UserRepository
from src.apps.auth.schemas import UserRead, UserCreate, UserUpdate
from src.db.base_db import get_session
from src.utils.base_depends import Pagination

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("", response_model=List[UserRead], summary="Get users", description="Get user list")
@cache(expire=30)
async def get_list(
    pagination: Pagination = Depends(Pagination),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await UserRepository(session).get_list_users(pagination.skip, pagination.limit)


@router.get("/{user_id}", response_model=UserRead, summary="Get user", description="Get user by id")
async def get_one(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await UserRepository(session).get_one_user(user_id)


@router.post("", response_model=UserRead, summary="Add user", description="Add new user")
async def add_one(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    return await UserRepository(session).add_one_user(user)


@router.patch("/{user_id}", response_model=UserRead, summary="Change user", description="Change user by id")
async def edit_one(
    user_id: uuid.UUID,
    user: UserUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await UserRepository(session).edit_one_user(user_id, user)


@router.delete("/{user_id}", summary="Delete user", description="Delete user by id")
async def delete_one(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await UserRepository(session).delete_one(user_id)


@router.get("/me/", response_model=UserRead, summary="Get me", description="Get my params")
async def get_me(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    print(UserRead)
    return await UserRepository(session).get_one(current_user.id)


@router.patch("/me/", response_model=UserRead, summary="Change me", description="Change my params")
async def edit_me(
    user: UserUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await UserRepository(session).edit_one_user(current_user.id, user)


@router.delete("/me/", summary="Delete me", description="Delete my params")
async def delete_me(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await UserRepository(session).deactivate_one(current_user.id)
