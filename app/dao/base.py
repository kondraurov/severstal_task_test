import logging

from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session_maker

logger = logging.getLogger(__name__)

class BaseDAO:
    model = None

    @staticmethod
    async def execute_query(query, session):
        try:
            logger.info(f"Выполняем запрос: {query}")
            result = await session.execute(query)
            return result
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при выполнении запроса: {e}")
            return None  # Не выбрасываем исключение, чтобы Swagger не падал с 500

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await cls.execute_query(query, session)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model)

            # Проверяем, есть ли фильтры, и применяем их через filter(), а не filter_by()
            if filter_by:
                query = query.filter(*(getattr(cls.model, key) == value for key, value in filter_by.items()))

            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            try:
                logger.info(f"Добавляем данные: {data}")

                # Создаем объект модели с правильными именами полей
                new_roll = cls.model(
                    length=data["length"],
                    weight=data["weight"],
                    added_date=data["added_date"],  # Используем правильное имя поля
                    removed_date=data.get("removed_date")  # Если отсутствует, будет None
                )

                session.add(new_roll)
                await session.commit()
                await session.refresh(new_roll)  # Обновляем объект, чтобы получить id

                return new_roll  # Возвращаем добавленный объект
            except SQLAlchemyError as e:
                logger.error(f"Ошибка при добавлении: {e}")
                raise HTTPException(status_code=500, detail="Ошибка базы данных")
