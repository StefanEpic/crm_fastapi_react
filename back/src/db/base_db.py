import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import DATABASE_URL
from sqlalchemy.dialects.postgresql import UUID

engine = create_async_engine(DATABASE_URL)


async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True
    )
