from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from .config import settings


async_engine = create_async_engine(
    url=settings.DATABASE_URL,
)

async_session = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
)

async def get_session():
    async with async_session() as session:
        yield session

class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)