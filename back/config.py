import os

from dotenv import load_dotenv

load_dotenv()
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

SQLADMIN_USER = os.environ.get("SQLADMIN_USER")
SQLADMIN_PASSWORD = os.environ.get("SQLADMIN_PASSWORD")
SQLADMIN_TOKEN = os.environ.get("SQLADMIN_TOKEN")

BASE_SITE_URL = os.environ.get("BASE_SITE_URL")
MEDIA_URL = f"{os.path.abspath(os.curdir)}/media"

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXP_DAYS = float(os.environ.get("JWT_ACCESS_TOKEN_EXP_DAYS"))
JWT_REFRESH_TOKEN_EXP_DAYS = float(os.environ.get("JWT_REFRESH_TOKEN_EXP_DAYS"))
