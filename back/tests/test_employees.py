from httpx import AsyncClient

from src.apps.auth.models import User
from src.apps.crm.models import Department, Employee
from tests.conftest import get_model_uuid

base_url = "/employees"


async def test_add_one_employee_invalid_user_name(auth_ac_admin: AsyncClient):
    user_id = await get_model_uuid(User, {"email": "employee@employee.com"})
    department_id = await get_model_uuid(Department, {"title": "Department1"})

    data = {
        "user_id": str(user_id),
        "family": "Family",
        "name": "Name2000",
        "surname": "Surname",
        "phone": "12345",
        "department_id": str(department_id),
    }
    response = await auth_ac_admin.post(base_url, json=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid value for family, name or surname fields"


async def test_add_one_employee_invalid_user_phone(auth_ac_admin: AsyncClient):
    user_id = await get_model_uuid(User, {"email": "employee@employee.com"})
    department_id = await get_model_uuid(Department, {"title": "Department1"})

    data = {
        "user_id": str(user_id),
        "family": "Family",
        "name": "Name",
        "surname": "Surname",
        "phone": "phone",
        "department_id": str(department_id),
    }
    response = await auth_ac_admin.post(base_url, json=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid value for phone field"


async def test_add_one_employee(auth_ac_admin: AsyncClient):
    user_id = await get_model_uuid(User, {"email": "employee@employee.com"})
    department_id = await get_model_uuid(Department, {"title": "Department1"})

    data = {
        "user_id": str(user_id),
        "family": "Family",
        "name": "Name",
        "surname": "Surname",
        "phone": "12345",
        "department_id": str(department_id),
    }
    response = await auth_ac_admin.post(base_url, json=data)

    assert response.status_code == 200
    assert response.json()["user_id"] == data["user_id"]


async def test_add_one_employee_invalid_user_unique(auth_ac_admin: AsyncClient):
    user_id = await get_model_uuid(User, {"email": "employee@employee.com"})
    department_id = await get_model_uuid(Department, {"title": "Department1"})

    data = {
        "user_id": str(user_id),
        "family": "Family",
        "name": "Name",
        "surname": "Surname",
        "phone": "123456",
        "department_id": str(department_id),
    }
    response = await auth_ac_admin.post(base_url, json=data)

    assert response.status_code == 400
    assert response.json()["detail"] == f"Key (user_id)=({user_id}) already exists."


async def test_get_list_employees(auth_ac_user: AsyncClient):
    response = await auth_ac_user.get(base_url)

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_list_employees_forbidden(auth_ac: AsyncClient):
    response = await auth_ac.get(base_url)

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


async def test_get_one_employee(auth_ac_user: AsyncClient):
    user_id = await get_model_uuid(User, {"email": "employee@employee.com"})
    uuid = str(await get_model_uuid(Employee, {"user_id": user_id}))
    uuid_url = base_url + "/" + uuid
    response = await auth_ac_user.get(uuid_url)

    assert response.status_code == 200
    assert response.json()["id"] == uuid


async def test_get_one_employee_forbidden(auth_ac: AsyncClient):
    user_id = await get_model_uuid(User, {"email": "employee@employee.com"})
    uuid = str(await get_model_uuid(Employee, {"user_id": user_id}))
    uuid_url = base_url + "/" + uuid
    response = await auth_ac.get(uuid_url)

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


async def test_edit_one_employee(auth_ac_admin: AsyncClient):
    user_id = await get_model_uuid(User, {"email": "employee@employee.com"})
    uuid = str(await get_model_uuid(Employee, {"user_id": user_id}))
    uuid_url = base_url + "/" + uuid
    data = {"family": "Test", "name": "Test", "surname": "Test"}
    response = await auth_ac_admin.patch(uuid_url, json=data)

    assert response.status_code == 200
    assert response.json()["family"] == data["family"]
    assert response.json()["name"] == data["name"]
    assert response.json()["surname"] == data["surname"]
    assert response.json()["id"] == uuid


async def test_edit_one_employee_forbidden(auth_ac_user: AsyncClient):
    user_id = await get_model_uuid(User, {"email": "employee@employee.com"})
    uuid = str(await get_model_uuid(Employee, {"user_id": user_id}))
    uuid_url = base_url + "/" + uuid
    data = {"family": "New Family", "name": "New Name", "surname": "New Surname"}
    response = await auth_ac_user.patch(uuid_url, json=data)

    assert response.status_code == 403
    assert response.json()["detail"] == "Don't have permissions"


async def test_delete_one_employee(auth_ac_admin: AsyncClient):
    user_id = await get_model_uuid(User, {"email": "employee@employee.com"})
    uuid = str(await get_model_uuid(Employee, {"user_id": user_id}))
    uuid_url = base_url + "/" + uuid
    response = await auth_ac_admin.delete(uuid_url)

    assert response.status_code == 200
    assert response.json()["detail"] == "success"


async def test_add_me(auth_ac_employee: AsyncClient):
    department_id = await get_model_uuid(Department, {"title": "Department1"})
    uuid_url = base_url + "/me/"

    data = {
        "family": "Family",
        "name": "Name",
        "surname": "Surname",
        "phone": "23456",
        "department_id": str(department_id),
    }
    response = await auth_ac_employee.post(uuid_url, json=data)

    assert response.status_code == 200
    assert response.json()["family"] == data["family"]


async def test_get_me(auth_ac_employee: AsyncClient):
    uuid_url = base_url + "/me/"
    response = await auth_ac_employee.get(uuid_url)

    assert response.status_code == 200
    assert response.json()["family"] == "Family"


async def test_edit_me(auth_ac_employee: AsyncClient):
    uuid_url = base_url + "/me/"
    data = {"family": "Employee"}
    response = await auth_ac_employee.patch(uuid_url, json=data)

    assert response.status_code == 200
    assert response.json()["family"] == data["family"]


async def test_delete_me(auth_ac_employee: AsyncClient):
    uuid_url = base_url + "/me/"
    response = await auth_ac_employee.delete(uuid_url)

    assert response.status_code == 200
    assert response.json()["detail"] == "success"


async def test_add_one_employee_inactive_user(auth_ac_employee: AsyncClient):
    user_id = await get_model_uuid(User, {"email": "employee@employee.com"})
    department_id = await get_model_uuid(Department, {"title": "Department1"})

    data = {
        "user_id": str(user_id),
        "family": "Family",
        "name": "Name",
        "surname": "Surname",
        "phone": "12345",
        "department_id": str(department_id),
    }
    response = await auth_ac_employee.post(base_url, json=data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"
