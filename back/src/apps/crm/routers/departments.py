import uuid
from typing import List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.auth.models import User
from src.apps.auth.permissions import check_permission_user, check_permission_moderator
from src.apps.crm.repositories import DepartmentRepository
from src.apps.crm.schemas import DepartmentRead, DepartmentCreate, DepartmentUpdate, DepartmentReadWithEmployees
from src.db.base_db import get_session
from src.base_utils.base_depends import Pagination

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


@router.get("", response_model=List[DepartmentRead])
@cache(expire=30)
async def get_list(
    pagination: Pagination = Depends(Pagination),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await DepartmentRepository(session).get_list(pagination.skip, pagination.limit)


@router.get("/{department_id}", response_model=DepartmentReadWithEmployees)
@cache(expire=30)
async def get_one(
    department_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await DepartmentRepository(session).get_one(department_id)


@router.post("", response_model=DepartmentRead)
async def add_one(
    department: DepartmentCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await DepartmentRepository(session).add_one(department)


@router.patch("/{department_id}", response_model=DepartmentRead)
async def edit_one(
    department_id: uuid.UUID,
    department: DepartmentUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await DepartmentRepository(session).edit_one(department_id, department)


@router.delete("/{department_id}")
async def delete_one(
    department_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await DepartmentRepository(session).delete_one(department_id)
