from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from secunda.infra.config import PostgresSettings


def new_session_maker(psql_config: PostgresSettings) -> async_sessionmaker[AsyncSession]:
    database_uri = psql_config.async_url()

    engine = create_async_engine(
        database_uri,
        pool_size=15,
        max_overflow=15,
        echo=False,
    )
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
