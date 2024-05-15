from __future__ import annotations
# Pydantic needs this import outside of a TYPE_CHECKIGN block
from fastapi.requests import HTTPConnection  # noqa: TCH002
from typing import Annotated, Callable, TYPE_CHECKING, AsyncIterator, Any
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import sessionmaker
from fastapi import Depends, FastAPI

from ..settings import DBSettings
from ..utils import as_list

if TYPE_CHECKING:
    from sqlalchemy.sql.schema import MetaData

__all__ = ["Session", "db_lifespan", "database_session"]


# HTTPConnection -> works for Request and Websocket
async def database_session(connection: HTTPConnection) -> AsyncIterator[AsyncSession]:
    session: AsyncSession = connection.state.sessionmaker()
    # for auto-commiting:
    # async with session.begin():
    #    yield session
    try:
        yield session
    # except:
    # await session.rollback()
    #    raise
    finally:
        await session.close()


# example usage:
Session = Annotated[AsyncSession, Depends(database_session)]


@asynccontextmanager
async def db_lifespan(
    app: FastAPI,  # noqa: ARG001
    settings: DBSettings | None = None,
    create_metadata: MetaData | list[MetaData] | None = None,
    init_hook: Callable | None = None,
    execution_options: dict | None = None,
    **kwargs,
) -> AsyncIterator[dict[str, Any]]:
    if settings is None:
        settings = DBSettings()  # pyright: ignore[reportCallIssue]
    engine = settings.create_async_engine(execution_options=execution_options)
    # pyright ignores because sessionmaker typing is scuffed for async
    app_sessionmaker: sessionmaker[AsyncSession] = sessionmaker(  # pyright: ignore
        engine,  # pyright: ignore
        class_=AsyncSession,
        **kwargs,
    )
    if create_metadata:
        async with engine.begin() as conn:
            for metadata in as_list(create_metadata):
                await conn.run_sync(metadata.create_all)
    if init_hook is not None:
        async with app_sessionmaker() as session:
            await init_hook(session)
    yield {"engine": engine, "sessionmaker": app_sessionmaker}
