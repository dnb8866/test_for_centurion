from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from utils.entities import Db


class SqlAlchemyDb(Db):
    def __init__(self, sql_url, base: type[DeclarativeBase], test: bool = False):
        self.metadata = base.metadata
        self.engine = create_async_engine(
            sql_url,
            poolclass=NullPool if test else None,
            echo=False
        )
        self.SessionLocal = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def prepare(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.create_all)

    async def clean(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.drop_all)

