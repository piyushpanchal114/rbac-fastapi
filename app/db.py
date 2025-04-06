import contextlib
import os
from typing import Any, AsyncIterator, AsyncGenerator
from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker, AsyncSession)


class DatabaseSessionManager:
    """Database session manager"""

    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            bind=self._engine, expire_on_commit=False)

    async def close(self):
        if self._engine is None:
            raise Exception("Database session manager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncSession]:
        if self._engine is None:
            raise Exception("Database session manager is not initialized")
        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception:
                await conn.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("Database session manager is not initialized")
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


db_url = os.environ.get("DB_URL")
echo_sql = bool(int(os.environ.get("ECHO_SQL", 0)))

sessionmanager = DatabaseSessionManager(db_url, {"echo": echo_sql})


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmanager.session() as session:
        yield session
