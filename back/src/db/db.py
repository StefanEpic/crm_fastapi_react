from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)


async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
