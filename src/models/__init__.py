from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from quart_bcrypt import Bcrypt
from src.config import config
bcrypt = Bcrypt()
# SQLALCHEMY_DATABASE_URI is "postgresql+psycopg://...": psycopg 3 provides both the sync and async drivers.
engine = create_async_engine(config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
# expire_on_commit=False: after commit() the instances keep their loaded attribute values. Otherwise accessing
# an attribute would trigger an implicit lazy refresh (blocking IO) which is not allowed with AsyncSession.
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
