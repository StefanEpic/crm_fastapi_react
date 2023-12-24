import os

from dotenv import load_dotenv

load_dotenv()
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")

# DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL = 'sqlite+aiosqlite:///sqlite.db'

POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

SQLADMIN_USER = os.environ.get("SQLADMIN_USER")
SQLADMIN_PASSWORD = os.environ.get("SQLADMIN_PASSWORD")

SITE_URL = os.environ.get("SITE_URL")
MEDIA_URL = f'{os.path.abspath(os.curdir)}/media'

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

SENTRY_TOKEN = os.environ.get("SENTRY_TOKEN")