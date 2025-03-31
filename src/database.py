from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

DATABASE_URL = settings.get_db_url()
engine = create_async_engine(DATABASE_URL, echo=True)

new_async_sess = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_async_sess() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
