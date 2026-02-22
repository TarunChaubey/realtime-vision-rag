from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from typing import AsyncGenerator
from src.core.config import settings

engine = create_async_engine(settings.async_db_url, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    # Import all models so Base.metadata is populated
    from src.models.base import Base
    import src.models.video   # noqa
    import src.models.frame   # noqa
    import src.models.image   # noqa
    import src.models.rag     # noqa

    async with engine.begin() as conn:
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {settings.SCHEMA_NAME}"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS multi_modal_rag"))
        await conn.run_sync(Base.metadata.create_all)
