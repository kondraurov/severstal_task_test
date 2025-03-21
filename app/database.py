from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.exc import OperationalError

database_url = "sqlite+aiosqlite:////app/db.sqlite3"
engine = create_async_engine(url=database_url, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

async def test_db_connection():
    try:
        async with engine.connect() as conn:
            await conn.run_sync(lambda connection: print("Подключение к базе данных успешно!"))
        return True
    except OperationalError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return False
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return False