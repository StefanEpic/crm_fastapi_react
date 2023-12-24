from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from prometheus_fastapi_instrumentator import Instrumentator

# from redis import asyncio as aioredis

from sqladmin import Admin

from src.routers import all_routers
from src.sqladmin.views import all_views, authentication_backend
from src.db.db import engine


app = FastAPI(title="Kanban")

for router in all_routers:
    app.include_router(router)

admin = Admin(app, engine, title='Kanban Admin Panel', authentication_backend=authentication_backend)

for view in all_views:
    admin.add_view(view)

origins = [
    "http://localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

Instrumentator().instrument(app).expose(app)

#
# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://redis")
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")