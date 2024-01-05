import os

from httpx import AsyncClient

from src.apps.crm.models import Employee, Department, Photo
from tests.conftest import get_model_uuid

base_url = "/photos"


async def test_init_employee_admin(auth_ac_admin: AsyncClient):
    department_id = await get_model_uuid(Department, {"title": "Department1"})
    uuid_url = "/employees/me/"

    data = {
        "family": "Admin",
        "name": "Admin",
        "surname": "Admin",
        "phone": "123456",
        "department_id": str(department_id),
    }
    await auth_ac_admin.post(uuid_url, json=data)


async def test_init_employee_user(auth_ac_user: AsyncClient):
    department_id = await get_model_uuid(Department, {"title": "Department1"})
    uuid_url = "/employees/me/"

    data = {
        "family": "User",
        "name": "User",
        "surname": "User",
        "phone": "1234567",
        "department_id": str(department_id),
    }
    await auth_ac_user.post(uuid_url, json=data)


async def test_add_one_photo(auth_ac_admin: AsyncClient):
    uuid = str(await get_model_uuid(Employee, {"family": "Admin"}))
    uuid_url = base_url + "/" + uuid
    filepath = f"{os.path.abspath(os.curdir)}/tests/testfile.jpeg"
    with open(filepath, "rb") as photo:
        response = await auth_ac_admin.put(uuid_url, params={"employee_id": uuid}, files={"photo": photo})

        assert response.status_code == 200
        assert response.json()["employee_id"] == uuid


async def test_get_list_photos(auth_ac_user: AsyncClient):
    response = await auth_ac_user.get(base_url)

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_one_photo(auth_ac_user: AsyncClient):
    employee_id = str(await get_model_uuid(Employee, {"family": "Admin"}))
    photo_id = str(await get_model_uuid(Photo, {"employee_id": employee_id}))
    uuid_url = base_url + "/" + photo_id
    response = await auth_ac_user.get(uuid_url)

    assert response.status_code == 200


async def test_delete_one_photo(auth_ac_admin: AsyncClient):
    employee_id = str(await get_model_uuid(Employee, {"family": "Admin"}))
    photo_id = str(await get_model_uuid(Photo, {"employee_id": employee_id}))
    uuid_url = base_url + "/" + photo_id
    response = await auth_ac_admin.delete(uuid_url)

    assert response.status_code == 200
    assert response.json()["detail"] == "success"


async def test_add_one_photo_my(auth_ac_user: AsyncClient):
    employee_id = str(await get_model_uuid(Employee, {"family": "User"}))
    uuid_url = base_url + "/my/"
    filepath = f"{os.path.abspath(os.curdir)}/tests/testfile.jpeg"
    with open(filepath, "rb") as photo:
        response = await auth_ac_user.put(uuid_url, files={"photo": photo})

    assert response.status_code == 200
    assert response.json()['employee_id'] == employee_id


async def test_delete_one_photo_my(auth_ac_user: AsyncClient):
    uuid_url = base_url + "/my/"
    response = await auth_ac_user.delete(uuid_url)

    assert response.status_code == 200
    assert response.json()['detail'] == 'success'
