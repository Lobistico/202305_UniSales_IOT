from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from core.configs import settings
engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session: AsyncSession = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)