from httpx import AsyncClient

from src.apps.crm.models import Project
from tests.conftest import get_model_uuid

base_url = "/projects"


async def test_add_one_project(auth_ac_admin: AsyncClient):
    data = {"title": "New project"}
    response = await auth_ac_admin.post(base_url, json=data)

    assert response.status_code == 200
    assert response.json()["title"] == data["title"]


async def test_add_one_project_invalid_title_unique(auth_ac_admin: AsyncClient):
    data = {"title": "New project"}
    response = await auth_ac_admin.post(base_url, json=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "UNIQUE constraint failed: project.title"


async def test_get_list_projects(auth_ac_user: AsyncClient):
    response = await auth_ac_user.get(base_url)

    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_get_one_project(auth_ac_user: AsyncClient):
    uuid = str(await get_model_uuid(Project, {"title": "Project1"}))
    uuid_url = base_url + "/" + uuid
    response = await auth_ac_user.get(uuid_url)

    assert response.status_code == 200
    assert response.json()["id"] == uuid


async def test_edit_one_project(auth_ac_admin: AsyncClient):
    uuid = str(await get_model_uuid(Project, {"title": "New project"}))
    uuid_url = base_url + "/" + uuid
    data = {"title": "Changed title"}
    response = await auth_ac_admin.patch(uuid_url, json=data)

    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["id"] == uuid


async def test_delete_one_project(auth_ac_admin: AsyncClient):
    uuid = str(await get_model_uuid(Project, {"title": "Changed title"}))
    uuid_url = base_url + "/" + uuid
    response = await auth_ac_admin.delete(uuid_url)

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
