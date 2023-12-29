import uuid
from typing import List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.auth.models import User
from src.apps.auth.permissions import check_permission_user, check_permission_moderator
from src.apps.crm.repositories import ProjectRepository
from src.apps.crm.schemas import ProjectRead, ProjectReadWithTasks, ProjectCreate, ProjectUpdate
from src.db.base_db import get_session
from src.base_utils.base_depends import Pagination

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get("", response_model=List[ProjectRead])
@cache(expire=30)
async def get_list(
    pagination: Pagination = Depends(Pagination),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await ProjectRepository(session).get_list_without_inactive(pagination.skip, pagination.limit)


@router.get("/{project_id}", response_model=ProjectReadWithTasks)
@cache(expire=30)
async def get_one(
    project_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_user),
):
    return await ProjectRepository(session).get_one_without_inactive(project_id)


@router.post("", response_model=ProjectRead)
async def add_one(
    project: ProjectCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await ProjectRepository(session).add_one(project)


@router.patch("/{project_id}", response_model=ProjectRead)
async def edit_one(
    project_id: uuid.UUID,
    project: ProjectUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await ProjectRepository(session).edit_one(project_id, project)


@router.delete("/{project_id}")
async def delete_one(
    project_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(check_permission_moderator),
):
    return await ProjectRepository(session).deactivate_one(project_id)
