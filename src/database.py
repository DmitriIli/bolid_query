from src.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine



sync_engine = create_engine(
    url = settings.DATABASE_URL_pyodbc,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

async_engine = create_async_engine(
    url = settings.DATABASE_URL_aioodbc,
    echo=True,
    pool_size=5,
    max_overflow=10,
)
