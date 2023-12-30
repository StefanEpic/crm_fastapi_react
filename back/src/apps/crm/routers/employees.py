import uuid
from typing import List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.auth.models import User
from src.apps.auth.permissions import check_permission_user, check_permission_moderator
from src.apps.auth.repositories import UserRepository
from src.apps.crm.repositories import EmployeeRepository
from src.apps.crm.schemas import (
    EmployeeRead,
    EmployeeReadWithTasks,
    EmployeeCreate,
    EmployeeUpdate,
    MyEmployeeCreate,
    MyEmployeeUpdate,
)
from src.db.base_db import get_session
from src.base_utils.base_depends import Pagination

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.get("", response_model=List[EmployeeRead])
@cache(expire=30)
async def get_list(
    pagination: Pagination = Depends(Pagination),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await EmployeeRepository(session).get_list_employees(pagination.skip, pagination.limit)


@router.get("/{employee_id}", response_model=EmployeeReadWithTasks)
@cache(expire=30)
async def get_one(
    employee_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await EmployeeRepository(session).get_one_employee(employee_id)


@router.post("", response_model=EmployeeRead)
async def add_one(
    employee: EmployeeCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await EmployeeRepository(session).add_one(employee)


@router.patch("/{employee_id}", response_model=EmployeeRead)
async def edit_one(
    employee_id: uuid.UUID,
    employee: EmployeeUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await EmployeeRepository(session).edit_one(employee_id, employee)


@router.delete("/{employee_id}")
async def delete_one(
    employee_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await EmployeeRepository(session).deactivate_one_employee(employee_id)


@router.get("/me/", response_model=EmployeeReadWithTasks)
@cache(expire=30)
async def get_one_employee_me(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await EmployeeRepository(session).get_one_employee_me(current_user.id)


@router.post("/me/", response_model=EmployeeRead)
async def add_one_me(
    employee: MyEmployeeCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await EmployeeRepository(session).add_one(employee, current_user.id)


@router.patch("/me/", response_model=EmployeeRead)
async def edit_one_me(
    employee: MyEmployeeUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await EmployeeRepository(session).edit_one_employee_me(current_user.id, employee)


@router.delete("/me/")
async def delete_me(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await UserRepository(session).deactivate_one(current_user.id)
