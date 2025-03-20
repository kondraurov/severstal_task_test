import logging
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session_maker

logger = logging.getLogger(__name__)

class BaseDAO:
    model = None

    @staticmethod
    async def execute_query(query, session):
        try:
            result = await session.execute(query)
            return result
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при выполнении запроса: {e}")
            raise e

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await cls.execute_query(query, session)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await cls.execute_query(query, session)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            try:
                insert_query = insert(cls.model).values(data)
                result = await cls.execute_query(insert_query, session)
                await session.commit()

                select_query = select(cls.model).filter_by(id=result.inserted_primary_key[0])
                inserted_item = await cls.execute_query(select_query, session)
                return inserted_item.scalar_one_or_none()
            except SQLAlchemyError as e:
                logger.error(f"Ошибка при добавлении: {e}")
                raise e
