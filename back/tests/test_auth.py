from httpx import AsyncClient


async def test_get_access_token(auth_ac: AsyncClient):
    data = {"email": "user@user.com", "password": "12345"}
    response = await auth_ac.post("/access", json=data)

    assert response.status_code == 200
    assert response.json()["email"] == data["email"]
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


async def test_get_access_token_invalid_email(auth_ac: AsyncClient):
    data = {"email": "user5@user.com", "password": "12345"}
    response = await auth_ac.post("/access", json=data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authorization credentials"


async def test_get_access_token_invalid_password(auth_ac: AsyncClient):
    data = {"email": "user@user.com", "password": "123456"}
    response = await auth_ac.post("/access", json=data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authorization credentials"


async def test_get_refresh_token(auth_ac: AsyncClient):
    data = {"email": "user@user.com", "password": "12345"}
    response = await auth_ac.post("/access", json=data)
    refresh_token = response.json()["refresh_token"]

    refresh_data = {"refresh_token": refresh_token}
    response = await auth_ac.post("/refresh", json=refresh_data)

    assert response.status_code == 200
    assert response.json()["email"] == data["email"]
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


async def test_get_refresh_token_invalid(auth_ac: AsyncClient):
    data = {"email": "user@user.com", "password": "12345"}
    response = await auth_ac.post("/access", json=data)
    refresh_token = response.json()["refresh_token"]
    refresh_token = refresh_token[:-1]

    refresh_data = {"refresh_token": refresh_token}
    response = await auth_ac.post("/refresh", json=refresh_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authorization credentials"
