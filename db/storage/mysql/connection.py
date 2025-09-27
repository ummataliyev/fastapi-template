"""
MySQL DB configurations
"""

from urllib.parse import quote

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from libs.environs import env


Base = declarative_base()


DB_USER = env.str("DB_USER")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.int("DB_PORT")
DB_PASSWORD = quote(env.str("DB_PASSWORD"))

DB_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    url=DB_URL,
    echo=True,
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """
    Dependency to get DB session.
    """
    async with async_session() as session:
        yield session
