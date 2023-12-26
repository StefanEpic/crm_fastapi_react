import uuid
from typing import List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.auth.models import User
from src.apps.auth.permissions import check_permission_user, check_permission_moderator
from src.apps.crm.repositories import PhotoRepository
from src.apps.crm.schemas import PhotoRead, PhotoCreate, PhotoUpdate
from src.db.db import get_session
from src.utils.base_depends import Pagination

router = APIRouter(
    prefix="/photos",
    tags=["Photos"],
)


@router.get("", response_model=List[PhotoRead])
@cache(expire=30)
async def get_list(
        pagination: Pagination = Depends(Pagination),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(check_permission_user),
):
    return await PhotoRepository(session).get_list(pagination.skip, pagination.limit)


@router.get("/{photo_id}", response_model=PhotoRead)
@cache(expire=30)
async def get_one(
        photo_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(check_permission_user),
):
    return await PhotoRepository(session).get_one(photo_id)


@router.post("", response_model=PhotoRead)
async def add_one(
        photo: PhotoCreate,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(check_permission_moderator),
):
    return await PhotoRepository(session).add_one(photo)


@router.patch("/{photo_id}", response_model=PhotoRead)
async def edit_one(
        photo_id: uuid.UUID,
        photo: PhotoUpdate,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(check_permission_moderator),
):
    return await PhotoRepository(session).edit_one(photo_id, photo)


@router.delete("/{photo_id}")
async def delete_one(
        photo_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(check_permission_moderator),
):
    return await PhotoRepository(session).delete_one(photo_id)


# @router.post("/my", response_model=PhotoRead)
# async def add_one(
#         photo: PhotoCreate,
#         session: AsyncSession = Depends(get_session),
#         current_user: User = Depends(check_permission_user),
# ):
#     return await PhotoRepository(session).add_one(photo)
#
#
# @router.patch("/my", response_model=PhotoRead)
# async def edit_one(
#         photo: PhotoUpdate,
#         session: AsyncSession = Depends(get_session),
#         current_user: User = Depends(check_permission_moderator),
# ):
#     photo_id =
#     return await PhotoRepository(session).edit_one(photo_id, photo)
#
#
# @router.delete("/my")
# async def delete_one(
#         photo_id: uuid.UUID,
#         session: AsyncSession = Depends(get_session),
#         current_user: User = Depends(check_permission_moderator),
# ):
#     return await PhotoRepository(session).delete_one(photo_id)
