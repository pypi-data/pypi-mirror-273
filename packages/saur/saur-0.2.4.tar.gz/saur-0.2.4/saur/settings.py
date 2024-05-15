from __future__ import annotations
from types import SimpleNamespace
from typing import Callable, Awaitable, TYPE_CHECKING
from functools import cached_property, partial

from sqlalchemy.engine import URL, Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm.session import Session, sessionmaker

from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from sqlalchemy.sql.schema import MetaData
    import pandas as pd

DIALECTS = SimpleNamespace(
    postgres=SimpleNamespace(
        sync_drivers=["psycopg2", "pg8000"],
        async_drivers=["asyncpg"],
    ),
    mysql=SimpleNamespace(
        sync_drivers=["mysqlclient", "mysqldb", "pymysql"],
        async_drivers=[None],
    ),
    sqlite=SimpleNamespace(
        sync_drivers=[None],
        async_drivers=["aiosqlite"],
    ),
)


def database_url(
    dialect: str,
    host: str,
    port: int | None = None,
    username: str | None = None,
    password: str | None = None,
    database: str | None = None,
    driver: str | None = None,
    query: dict[str, str | list[str]] = {},  # noqa: B006
    *,
    sync: bool = True,
) -> str:
    # cf https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
    # 'dialect+driver://username:password@host:port/database'
    if driver is None:
        if not hasattr(DIALECTS, dialect):
            msg = f"Cannot infer driver for dialect {dialect}."
            raise ValueError(msg)
        dialect_drivers = getattr(DIALECTS, dialect)
        # auto select driver
        if sync:
            driver = dialect_drivers.sync_drivers[0]
        else:
            driver = dialect_drivers.async_drivers[0]
    if driver is None:
        drivername = dialect
    else:
        drivername = f"{dialect}+{driver}"
    return URL.create(
        drivername=drivername,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
        query=query,
    ).render_as_string()


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    dialect: str
    host: str
    port: int | None = None  # port constraints?
    username: str | None = None
    password: str | None = None
    database: str | None = None
    driver: str | None = None
    echo: bool = False

    def url(self, *, sync: bool = True) -> str:
        settings = self.model_dump()
        settings.pop("echo")
        return database_url(sync=sync, **settings)


    def create_sync_engine(self, **kwargs) -> Engine:
        url = self.url(sync=False)
        kwargs.setdefault("echo", self.echo)
        return create_engine(url, **kwargs)

    def create_async_engine(self, **kwargs) -> AsyncEngine:
        url = self.url(sync=True)
        kwargs.setdefault("echo", self.echo)
        return create_async_engine(url, **kwargs)

    def create_engine(self, *, sync: bool = True, **kwargs) -> Engine | AsyncEngine:
        fn = self.create_sync_engine if sync else self.create_async_engine
        return fn(**kwargs)

    @cached_property
    def engine(self) -> Engine:
        return self.create_sync_engine()

    def sessionmaker(
        self,
        *,
        sync: bool = True,
        engine: Engine | AsyncEngine | None = None,
        **kwargs,
    ) -> sessionmaker[Session]:
        if engine is None:
            engine = self.create_engine(sync=sync)
        session_class = Session if sync else AsyncSession
        return sessionmaker(bind=engine, class_=session_class, **kwargs)  # pyright: ignore[reportCallIssue, reportArgumentType]

    def read_sql(self, sql: str, **kwargs) -> pd.DataFrame:
        import pandas as pd
        return pd.read_sql(sql, con=self.engine, **kwargs)

    def create_all(
        self,
        metadata: MetaData,
        *,
        sync: bool = True,
        engine: Engine | AsyncEngine | None = None,
    ) -> Callable[[], Awaitable | None]:
        if engine is None:
            engine = self.create_engine(sync=sync)
        if sync:
            if not isinstance(engine, Engine):
                msg = "Sync table creation requires sync engine"
                raise TypeError(msg)
            return partial(metadata.create_all, engine)
        if not isinstance(engine, AsyncEngine):
            msg = "Async table creation requires async engine"
            raise TypeError(msg)
        async def async_create_all() -> None:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)  # pylint: disable=no-member

        return async_create_all
