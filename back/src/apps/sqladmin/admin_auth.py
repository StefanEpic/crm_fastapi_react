from typing import Union
from jose import jwt
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from config import SQLADMIN_USER, SQLADMIN_PASSWORD, JWT_SECRET_KEY, JWT_ALGORITHM
from src.apps.auth.utils import create_access_jwt


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if username == SQLADMIN_USER and password == SQLADMIN_PASSWORD:
            access_token = await create_access_jwt(data={"user": SQLADMIN_USER, "pass": SQLADMIN_PASSWORD})
            request.session.update({"token": access_token})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Union[RedirectResponse, bool]:
        if "token" not in request.session:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        token = request.session["token"]
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload["user"] == SQLADMIN_USER and payload["pass"] == SQLADMIN_PASSWORD:
            return True


authentication_backend = AdminAuth(secret_key=JWT_SECRET_KEY)
