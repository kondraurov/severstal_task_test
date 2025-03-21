import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.database import Base

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"
engine = create_async_engine(DATABASE_URL, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("База данных успешно инициализирована!")

if __name__ == "__main__":
    asyncio.run(init_db())
