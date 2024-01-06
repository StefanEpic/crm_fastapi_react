from httpx import AsyncClient

from src.apps.crm.models import Department, Project, Employee, Task
from tests.conftest import get_model_uuid

base_url = "/tasks"


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


async def test_add_one_task(auth_ac_admin: AsyncClient):
    project_id = str(await get_model_uuid(Project, {"title": "Project1"}))
    employee_id = str(await get_model_uuid(Employee, {"family": "Admin"}))
    data = {"title": "Task1", "projects": [project_id], "employees": [employee_id], "author_id": employee_id}
    response = await auth_ac_admin.post(base_url, json=data)

    assert response.status_code == 200
    assert response.json()["title"] == data["title"]


async def test_get_list_tasks(auth_ac_user: AsyncClient):
    response = await auth_ac_user.get(base_url)

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_one_task(auth_ac_user: AsyncClient):
    uuid = str(await get_model_uuid(Task, {"title": "Task1"}))
    uuid_url = base_url + "/" + uuid
    response = await auth_ac_user.get(uuid_url)

    assert response.status_code == 200
    assert response.json()["id"] == uuid


async def test_edit_one_task(auth_ac_admin: AsyncClient):
    project_1_id = str(await get_model_uuid(Project, {"title": "Project1"}))
    project_2_id = str(await get_model_uuid(Project, {"title": "Project2"}))
    uuid = str(await get_model_uuid(Task, {"title": "Task1"}))
    uuid_url = base_url + "/" + uuid
    data = {"title": "Changed title", "projects": [project_1_id, project_2_id]}
    response = await auth_ac_admin.patch(uuid_url, json=data)

    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["projects"][0]["id"] == project_1_id
    assert response.json()["projects"][1]["id"] == project_2_id
    assert response.json()["id"] == uuid


async def test_delete_one_task(auth_ac_admin: AsyncClient):
    uuid = str(await get_model_uuid(Task, {"title": "Changed title"}))
    uuid_url = base_url + "/" + uuid
    response = await auth_ac_admin.delete(uuid_url)

    assert response.status_code == 200
    assert response.json()["detail"] == "success"


async def test_add_one_task_my(auth_ac_user: AsyncClient):
    project_id = str(await get_model_uuid(Project, {"title": "Project1"}))
    employee_id = str(await get_model_uuid(Employee, {"family": "Admin"}))
    data = {"title": "MyTask", "projects": [project_id], "employees": [employee_id]}
    uuid_url = base_url + "/my/"
    response = await auth_ac_user.post(uuid_url, json=data)

    assert response.status_code == 200
    assert response.json()["title"] == data["title"]


async def test_edit_one_task_my(auth_ac_user: AsyncClient):
    project_2_id = str(await get_model_uuid(Project, {"title": "Project2"}))
    uuid = str(await get_model_uuid(Task, {"title": "MyTask"}))
    uuid_url = base_url + "/my/" + uuid
    data = {"title": "My changed title", "projects": [project_2_id]}
    response = await auth_ac_user.patch(uuid_url, json=data)

    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["projects"][0]["id"] == project_2_id
    assert response.json()["id"] == uuid


async def test_delete_one_task_my(auth_ac_user: AsyncClient):
    uuid = str(await get_model_uuid(Task, {"title": "My changed title"}))
    uuid_url = base_url + "/my/" + uuid
    response = await auth_ac_user.delete(uuid_url)

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
