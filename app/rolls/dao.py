from datetime import date
from sqlalchemy import delete, func, select, cast, Date, case
from sqlalchemy.exc import SQLAlchemyError
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.rolls.models import Roll
import logging

logger = logging.getLogger(__name__)

class RollDAO(BaseDAO):
    model = Roll

    @classmethod
    async def find_by_filter(cls, **filters):
        try:
            async with async_session_maker() as session:
                query = select(cls.model)

                if filters.get("min_id") is not None:
                    query = query.filter(cls.model.id >= filters["min_id"])
                if filters.get("max_id") is not None:
                    query = query.filter(cls.model.id <= filters["max_id"])
                if filters.get("min_weight") is not None:
                    query = query.filter(cls.model.weight >= filters["min_weight"])
                if filters.get("max_weight") is not None:
                    query = query.filter(cls.model.weight <= filters["max_weight"])
                if filters.get("min_length") is not None:
                    query = query.filter(cls.model.length >= filters["min_length"])
                if filters.get("max_length") is not None:
                    query = query.filter(cls.model.length <= filters["max_length"])
                if filters.get("added_from") is not None:
                    query = query.filter(cls.model.added_date >= filters["added_from"])
                if filters.get("added_to") is not None:
                    query = query.filter(cls.model.added_date <= filters["added_to"])
                if filters.get("removed_from") is not None:
                    query = query.filter(cls.model.removed_date >= filters["removed_from"])
                if filters.get("removed_to") is not None:
                    query = query.filter(cls.model.removed_date <= filters["removed_to"])

                result = await session.execute(query)
                return result.mappings().all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при выполнении фильтрации: {e}")
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            raise

    @classmethod
    async def delete(cls, id_roll):
        try:
            async with async_session_maker() as session:
                stmt = delete(cls.model).where(cls.model.id == id_roll).returning(cls.model)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar()
        except SQLAlchemyError as e:
            logger.error(f"Error executing delete query: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    @classmethod
    async def getting_statistics(cls, start_date: date, end_date: date):
        try:
            async with async_session_maker() as session:
                logger.info(f"Start Date: {start_date}, End Date: {end_date}")

                # Используем func.julianday для работы с датами в SQLite
                max_storage_time_case = case(
                    (cls.model.removed_date.isnot(None),
                     func.julianday(cls.model.removed_date) - func.julianday(cls.model.added_date)),
                    else_=0
                )

                min_storage_time_case = case(
                    (cls.model.removed_date.isnot(None),
                     func.julianday(cls.model.removed_date) - func.julianday(cls.model.added_date)),
                    else_=0
                )

                # Запрос на статистику
                stats_query = select(
                    func.count(cls.model.id).label("added_count"),
                    func.count(cls.model.removed_date).label("removed_count"),
                    func.avg(cls.model.length).label("avg_length"),
                    func.avg(cls.model.weight).label("avg_weight"),
                    func.min(cls.model.length).label("min_length"),
                    func.max(cls.model.length).label("max_length"),
                    func.min(cls.model.weight).label("min_weight"),
                    func.max(cls.model.weight).label("max_weight"),
                    func.sum(cls.model.weight).label("total_weight"),
                    func.max(max_storage_time_case).label("max_storage_time"),
                    func.min(min_storage_time_case).label("min_storage_time"),
                ).where(
                    cls.model.added_date >= start_date,
                    cls.model.added_date <= end_date
                )

                logger.info(f"Executing stats query: {str(stats_query)}")

                result = await session.execute(stats_query)
                stats = result.fetchone()

                logger.info(f"Query result: {stats}")

                if not stats or stats[0] == 0:
                    return {
                        "added_count": 0,
                        "removed_count": 0,
                        "avg_length": None,
                        "avg_weight": None,
                        "min_length": None,
                        "max_length": None,
                        "min_weight": None,
                        "max_weight": None,
                        "total_weight": None,
                        "max_storage_time": None,
                        "min_storage_time": None,
                    }

                return {
                    "added_count": stats[0],
                    "removed_count": stats[1],
                    "avg_length": stats[2],
                    "avg_weight": stats[3],
                    "min_length": stats[4],
                    "max_length": stats[5],
                    "min_weight": stats[6],
                    "max_weight": stats[7],
                    "total_weight": stats[8],
                    "max_storage_time": stats[9],
                    "min_storage_time": stats[10],
                }

        except SQLAlchemyError as e:
            logger.error(f"Error executing statistics query: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise