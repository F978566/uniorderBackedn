from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


engine = create_async_engine("sqlite+aiosqlite:///uniorder.db", echo=True)


async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
