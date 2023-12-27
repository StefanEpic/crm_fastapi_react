from fastapi import FastAPI
from sqladmin import Admin
from fastapi.middleware.cors import CORSMiddleware

from src.apps.apps_routers import apps_routers
from src.apps.sqladmin.admin_auth import authentication_backend
from src.apps.sqladmin.routers import admin_routers
from src.db.db import engine

app = FastAPI(title="Kanban API", summary="API for Kanban task manager", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

admin = Admin(app, engine, title="Kanban Admin Panel", authentication_backend=authentication_backend)

for router in admin_routers:
    admin.add_view(router)


for router in apps_routers:
    app.include_router(router)
