from datetime import datetime
from sqlalchemy import delete, func, select
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

                if "min_id" in filters:
                    query = query.filter(cls.model.id >= filters["min_id"])
                if "max_id" in filters:
                    query = query.filter(cls.model.id <= filters["max_id"])
                if "min_weight" in filters:
                    query = query.filter(cls.model.weight >= filters["min_weight"])
                if "max_weight" in filters:
                    query = query.filter(cls.model.weight <= filters["max_weight"])
                if "min_length" in filters:
                    query = query.filter(cls.model.length >= filters["min_length"])
                if "max_length" in filters:
                    query = query.filter(cls.model.length <= filters["max_length"])
                if "added_from" in filters:
                    query = query.filter(cls.model.added_date >= filters["added_from"])
                if "added_to" in filters:
                    query = query.filter(cls.model.added_date <= filters["added_to"])
                if "removed_from" in filters:
                    query = query.filter(cls.model.removed_date >= filters["removed_from"])
                if "removed_to" in filters:
                    query = query.filter(cls.model.removed_date <= filters["removed_to"])

                result = await session.execute(query)
                return result.mappings().all()
        except SQLAlchemyError as e:
            logger.error(f"Error executing filter query: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    @classmethod
    async def delete(cls, id):
        try:
            async with async_session_maker() as session:
                stmt = delete(cls.model).where(cls.model.id == id).returning(cls.model)
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
    async def getting_statistics(cls, start_date: datetime, end_date: datetime):
        try:
            async with async_session_maker() as session:
                stats_query = select(
                    func.count().label("added_count"),
                    func.count(cls.model.removed_date.isnot(None)).label("removed_count"),
                    func.avg(cls.model.length).label("avg_length"),
                    func.avg(cls.model.weight).label("avg_weight"),
                    func.min(cls.model.length).label("min_length"),
                    func.max(cls.model.length).label("max_length"),
                    func.min(cls.model.weight).label("min_weight"),
                    func.max(cls.model.weight).label("max_weight"),
                    func.sum(cls.model.weight).label("total_weight"),
                    func.max(cls.model.removed_date - cls.model.added_date).label("max_storage_time"),
                    func.min(cls.model.removed_date - cls.model.added_date).label("min_storage_time"),
                    func.count(cls.model.added_date).label("min_rolls_day"),
                    func.count(cls.model.added_date).label("max_rolls_day"),
                    func.sum(cls.model.weight).label("min_weight_day"),
                    func.sum(cls.model.weight).label("max_weight_day")
                ).where(cls.model.added_date.between(start_date, end_date))

                result = await session.execute(stats_query)
                stats = result.fetchone()

                return {
                    "added_count": stats.added_count,
                    "removed_count": stats.removed_count,
                    "avg_length": stats.avg_length,
                    "avg_weight": stats.avg_weight,
                    "min_length": stats.min_length,
                    "max_length": stats.max_length,
                    "min_weight": stats.min_weight,
                    "max_weight": stats.max_weight,
                    "total_weight": stats.total_weight,
                    "max_storage_time": stats.max_storage_time,
                    "min_storage_time": stats.min_storage_time,
                    "min_rolls_day": stats.min_rolls_day,
                    "max_rolls_day": stats.max_rolls_day,
                    "min_weight_day": stats.min_weight_day,
                    "max_weight_day": stats.max_weight_day,
                }
        except SQLAlchemyError as e:
            logger.error(f"Error executing statistics query: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
