import asyncio
from asyncio import current_task
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine
)

from app.config import DATABASE_URL
from app.models import Base


async_engine = create_async_engine(DATABASE_URL, echo=False)
async_session_factory = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_scoped_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_scoped_session(
        async_session_factory,
        scopefunc=current_task,
    )
    try:
        yield async_session
    finally:
        await async_session.remove()
