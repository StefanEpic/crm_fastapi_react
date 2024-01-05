import uuid
from typing import List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.auth.models import User
from src.apps.auth.permissions import check_permission_user, check_permission_moderator
from src.apps.crm.repositories import TaskRepository
from src.apps.crm.schemas import (
    TaskRead,
    TaskReadWithProjectsAndEmployees,
    TaskCreate,
    TaskUpdate,
    MyTaskCreate,
    MyTaskUpdate,
)
from src.db.base_db import get_session
from src.base_utils.base_depends import Pagination

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("", response_model=List[TaskRead])
@cache(expire=30)
async def get_list(
    pagination: Pagination = Depends(Pagination),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await TaskRepository(session).get_list_without_inactive(pagination.skip, pagination.limit)


@router.get("/{task_id}", response_model=TaskReadWithProjectsAndEmployees)
@cache(expire=30)
async def get_one(
    task_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await TaskRepository(session).get_one_without_inactive(task_id)


@router.post("", response_model=TaskRead)
async def add_one(
    task: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await TaskRepository(session).add_one_task(task)


@router.patch("/{task_id}", response_model=TaskRead)
async def edit_one(
    task_id: uuid.UUID,
    task: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await TaskRepository(session).edit_one(task_id, task)


@router.delete("/{task_id}")
async def delete_one(
    task_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await TaskRepository(session).deactivate_one(task_id)


@router.post("/my/{task_id}", response_model=TaskRead)
async def add_one_me(
    task: MyTaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await TaskRepository(session).add_one_task_my(task, current_user.id)


@router.patch("/my/{task_id}", response_model=TaskRead)
async def edit_one_me(
    task: MyTaskUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await TaskRepository(session).edit_one_task_my(current_user.id, task)
