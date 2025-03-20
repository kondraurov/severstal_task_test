from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from app.database import test_db_connection
from app.rolls.router import router

@asynccontextmanager
async def lifespan(_):
    if not await test_db_connection():
        raise Exception("Не удалось подключиться к базе данных.")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
