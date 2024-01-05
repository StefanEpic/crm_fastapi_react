from httpx import AsyncClient

from src.apps.crm.models import Department
from tests.conftest import get_model_uuid

base_url = "/departments"


async def test_add_one_department(auth_ac_admin: AsyncClient):
    data = {"title": "New department"}
    response = await auth_ac_admin.post(base_url, json=data)

    assert response.status_code == 200
    assert response.json()["title"] == data["title"]


async def test_add_one_department_invalid_title_unique(auth_ac_admin: AsyncClient):
    data = {"title": "New department"}
    response = await auth_ac_admin.post(base_url, json=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Key (title)=(New department) already exists."


async def test_get_list_departments(auth_ac_user: AsyncClient):
    response = await auth_ac_user.get(base_url)

    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_get_one_department(auth_ac_user: AsyncClient):
    uuid = str(await get_model_uuid(Department, {"title": "Department1"}))
    uuid_url = base_url + "/" + uuid
    response = await auth_ac_user.get(uuid_url)

    assert response.status_code == 200
    assert response.json()["id"] == uuid


async def test_edit_one_department(auth_ac_admin: AsyncClient):
    uuid = str(await get_model_uuid(Department, {"title": "New department"}))
    uuid_url = base_url + "/" + uuid
    data = {"title": "Changed title"}
    response = await auth_ac_admin.patch(uuid_url, json=data)

    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["id"] == uuid


async def test_delete_one_department(auth_ac_admin: AsyncClient):
    uuid = str(await get_model_uuid(Department, {"title": "Changed title"}))
    uuid_url = base_url + "/" + uuid
    response = await auth_ac_admin.delete(uuid_url)

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
