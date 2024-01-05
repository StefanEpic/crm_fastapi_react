import asyncio
import uuid
from typing import AsyncGenerator
import pytest
import redis
from fastapi_cache import FastAPICache
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from main import app
from src.apps.auth.repositories import AuthRepository, UserRepository
from src.apps.auth.schemas import UserCreate
from src.apps.crm.repositories import DepartmentRepository, ProjectRepository
from src.apps.crm.schemas import DepartmentCreate, ProjectCreate
from src.db.base_db import engine, Base

client = TestClient(app)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        admin = UserCreate(email="admin@admin.com", password="12345")
        user = UserCreate(email="user@user.com", password="12345")
        employee = UserCreate(email="employee@employee.com", password="12345")
        employee2 = UserCreate(email="employee2@employee.com", password="12345")
        department1 = DepartmentCreate(title="Department1")
        department2 = DepartmentCreate(title="Department2")
        project1 = ProjectCreate(title="Project1")
        project2 = ProjectCreate(title="Project2")
        res_admin = await UserRepository(session).add_one_user(admin)
        res_user = await UserRepository(session).add_one_user(user)
        res_employee = await UserRepository(session).add_one_user(employee)
        res_employee2 = await UserRepository(session).add_one_user(employee2)
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

        res_employee.is_verify = True
        res_employee.permission = "user"
        session.add(res_employee)

        res_employee2.is_verify = True
        res_employee2.permission = "user"
        session.add(res_employee2)
        await session.commit()

        yield
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


async def get_token(data: UserCreate) -> str:
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        token = await AuthRepository(session).get_access_token(data)
        return token.access_token


@pytest.fixture(scope="session")
async def auth_ac() -> AsyncGenerator[AsyncClient, None]:
    """
    Create anonim user
    :return: AsyncClient
    """
    async with AsyncClient(app=app, base_url="http://test") as auth_ac:
        yield auth_ac


@pytest.fixture(scope="session")
async def auth_ac_admin() -> AsyncGenerator[AsyncClient, None]:
    """
    Create admin user
    :return: AsyncClient
    """
    async with AsyncClient(app=app, base_url="http://test") as auth_ac_admin:
        user_data = UserCreate(email="admin@admin.com", password="12345")
        token = await get_token(user_data)
        auth_headers = {"Authorization": f"Bearer {token}"}
        auth_ac_admin.headers.update(auth_headers)
        yield auth_ac_admin


@pytest.fixture(scope="session")
async def auth_ac_user() -> AsyncGenerator[AsyncClient, None]:
    """
    Create authorization user
    :return: AsyncClient
    """
    async with AsyncClient(app=app, base_url="http://test") as auth_ac_user:
        user_data = UserCreate(email="user@user.com", password="12345")
        token = await get_token(user_data)
        auth_headers = {"Authorization": f"Bearer {token}"}
        auth_ac_user.headers.update(auth_headers)
        yield auth_ac_user


@pytest.fixture(scope="session")
async def auth_ac_employee() -> AsyncGenerator[AsyncClient, None]:
    """
    Create authorization employee
    :return: AsyncClient
    """
    async with AsyncClient(app=app, base_url="http://test") as auth_ac_employee:
        user_data = UserCreate(email="employee2@employee.com", password="12345")
        token = await get_token(user_data)
        auth_headers = {"Authorization": f"Bearer {token}"}
        auth_ac_employee.headers.update(auth_headers)
        yield auth_ac_employee


@pytest.fixture(scope="session", autouse=True)
def cache_init():
    redis_client = redis.Redis(host="localhost", port=6379)
    FastAPICache.init(backend=redis_client)


async def get_model_uuid(model: Base, filter_params) -> uuid.UUID:
    """
    Take UUID of model exemplar
    :param model: model
    :param filter_params: params for filter
    :return: UUID
    """
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        stmt = select(model).filter_by(**filter_params)
        res = await session.execute(stmt)
        res = res.scalar_one()
        return res.id
