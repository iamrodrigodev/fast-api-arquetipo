from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from app.core.config.ajustes import ajustes

usar_null_pool = ajustes.ENTORNO.lower() in {"dev", "test", "testing", "local"}

engine = create_async_engine(
    ajustes.DATABASE_URL,
    echo=False,
    future=True,
    poolclass=NullPool if usar_null_pool else None
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

from typing import AsyncGenerator

async def obtener_bd() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
