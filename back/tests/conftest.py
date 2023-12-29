import asyncio
import uuid
from typing import AsyncGenerator
import pytest
import redis
from fastapi_cache import FastAPICache
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from main import app
from src.apps.auth.repositories import AuthRepository, UserRepository
from src.apps.auth.schemas import UserCreate
from src.apps.crm.models import Department, Project
from src.apps.crm.repositories import DepartmentRepository, ProjectRepository
from src.apps.crm.schemas import DepartmentCreate, ProjectCreate
from src.db.base_db import Base, get_session

engine_test = create_async_engine("sqlite+aiosqlite:///test.db")
Base.metadata.bind = engine_test
client = TestClient(app)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_async_session


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        async_session = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            admin = UserCreate(email="admin@admin.com", password="12345")
            user = UserCreate(email="user@user.com", password="12345")
            department1 = DepartmentCreate(title="Department1")
            department2 = DepartmentCreate(title="Department2")
            project1 = ProjectCreate(title="Project1")
            project2 = ProjectCreate(title="Project2")
            res_admin = await UserRepository(session).add_one_user(admin)
            res_user = await UserRepository(session).add_one_user(user)
            await DepartmentRepository(session).add_one(department1)
            await DepartmentRepository(session).add_one(department2)
            await ProjectRepository(session).add_one(project1)
            await ProjectRepository(session).add_one(project2)
            await session.commit()

            res_admin.is_verify = True
            res_admin.permission = "admin"
            session.add(res_admin)

            res_user.is_verify = True
            res_user.permission = "user"
            session.add(res_user)
            await session.commit()

    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


async def get_token(data: UserCreate) -> str:
    async_session = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        token = await AuthRepository(session).get_access_token(data)
        return token.access_token


@pytest.fixture(scope="session")
async def auth_ac_admin() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as auth_ac_admin:
        user_data = UserCreate(email="admin@admin.com", password="12345")
        token = await get_token(user_data)
        auth_headers = {"Authorization": f"Bearer {token}"}
        auth_ac_admin.headers.update(auth_headers)
        yield auth_ac_admin


@pytest.fixture(scope="session")
async def auth_ac_user() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as auth_ac_user:
        user_data = UserCreate(email="user@user.com", password="12345")
        token = await get_token(user_data)
        auth_headers = {"Authorization": f"Bearer {token}"}
        auth_ac_user.headers.update(auth_headers)
        yield auth_ac_user


@pytest.fixture(scope="session", autouse=True)
def cache_init():
    redis_client = redis.Redis(host="localhost", port=6379)
    FastAPICache.init(backend=redis_client)


async def get_department_id(title: str) -> uuid.UUID:
    async_session = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        stmt = select(Department).where(Department.title == title)
        department = await session.execute(stmt)
        department = department.scalar_one()
        return department.id


async def get_project_id(title: str) -> uuid.UUID:
    async_session = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        stmt = select(Project).where(Project.title == title)
        project = await session.execute(stmt)
        project = project.scalar_one()
        return project.id
