import uuid
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.auth.models import User
from src.apps.auth.permissions import check_permission_user, check_permission_moderator
from src.apps.crm.repositories import PhotoRepository
from src.apps.crm.schemas import PhotoRead
from src.db.base_db import get_session
from src.base_utils.base_depends import Pagination

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


@router.put("/{photo_id}", response_model=PhotoRead)
async def put_one(
    employee_id: uuid.UUID,
    photo: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await PhotoRepository(session).put_one_photo(employee_id, photo)


@router.delete("/{photo_id}")
async def delete_one(
    photo_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await PhotoRepository(session).delete_one_photo(photo_id)


@router.put("/my/", response_model=PhotoRead)
async def put_one_my(
    photo: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await PhotoRepository(session).put_one_photo_my(current_user.id, photo)


@router.delete("/my/")
async def delete_one_my(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await PhotoRepository(session).delete_one_photo(current_user.id)
