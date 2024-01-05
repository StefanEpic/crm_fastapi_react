from httpx import AsyncClient

from src.apps.auth.models import User
from tests.conftest import get_model_uuid

base_url = "/users"


async def test_add_one_user(auth_ac: AsyncClient):
    data = {"email": "test@test.com", "password": "12345"}
    response = await auth_ac.post(base_url, json=data)

    assert response.status_code == 200
    assert response.json()["email"] == data["email"]


async def test_add_one_user_invalid_email_unique(auth_ac: AsyncClient):
    data = {"email": "test@test.com", "password": "12345"}
    response = await auth_ac.post(base_url, json=data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Key (email)=(test@test.com) already exists."


async def test_get_list_users(auth_ac_user: AsyncClient):
    response = await auth_ac_user.get(base_url)

    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_one_user(auth_ac_admin: AsyncClient):
    uuid = str(await get_model_uuid(User, {"email": "user@user.com"}))
    uuid_url = base_url + "/" + uuid
    response = await auth_ac_admin.get(uuid_url)

    assert response.status_code == 200
    assert response.json()["id"] == uuid


async def test_get_one_user_forbidden(auth_ac_user: AsyncClient):
    uuid = str(await get_model_uuid(User, {"email": "user@user.com"}))
    uuid_url = base_url + "/" + uuid
    response = await auth_ac_user.get(uuid_url)

    assert response.status_code == 403
    assert response.json()["detail"] == "Don't have permissions"


async def test_edit_one_user(auth_ac_admin: AsyncClient):
    uuid = str(await get_model_uuid(User, {"email": "test@test.com"}))
    uuid_url = base_url + "/" + uuid
    data = {"email": "test2@test.com"}
    response = await auth_ac_admin.patch(uuid_url, json=data)

    assert response.status_code == 200
    assert response.json()["email"] == data["email"]
    assert response.json()["id"] == uuid


async def test_edit_one_user_forbidden(auth_ac_user: AsyncClient):
    uuid = str(await get_model_uuid(User, {"email": "admin@admin.com"}))
    uuid_url = base_url + "/" + uuid
    data = {"email": "admin2@admin.com"}
    response = await auth_ac_user.patch(uuid_url, json=data)

    assert response.status_code == 403
    assert response.json()["detail"] == "Don't have permissions"


async def test_delete_one_user(auth_ac_admin: AsyncClient):
    uuid = str(await get_model_uuid(User, {"email": "test2@test.com"}))
    uuid_url = base_url + "/" + uuid
    response = await auth_ac_admin.delete(uuid_url)

    assert response.status_code == 200
    assert response.json()["detail"] == "success"


async def test_get_me(auth_ac_user: AsyncClient):
    uuid_url = base_url + "/me/"
    response = await auth_ac_user.get(uuid_url)

    assert response.status_code == 200
    assert response.json()["email"] == "user@user.com"


async def test_edit_me(auth_ac_user: AsyncClient):
    uuid_url = base_url + "/me/"
    data = {"email": "user2@user.com"}
    response = await auth_ac_user.patch(uuid_url, json=data)

    assert response.status_code == 200
    assert response.json()["email"] == data["email"]


async def test_return_user(auth_ac_admin: AsyncClient):
    uuid = str(await get_model_uuid(User, {"email": "user2@user.com"}))
    uuid_url = base_url + "/" + uuid
    data = {"email": "user@user.com"}
    response = await auth_ac_admin.patch(uuid_url, json=data)

    assert response.status_code == 200
    assert response.json()["email"] == data["email"]
    assert response.json()["id"] == uuid


async def test_delete_me(auth_ac_user: AsyncClient):
    uuid_url = base_url + "/me/"
    response = await auth_ac_user.delete(uuid_url)

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
