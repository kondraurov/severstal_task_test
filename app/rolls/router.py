from datetime import date
from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from sqlalchemy import select

from app.database import async_session_maker
from app.rolls.schemas import SchemasRoll
from app.rolls.dao import RollDAO
from app.rolls.services import filter_roll, delete_roll
from app.rolls.models import RollFilter, Roll

router = APIRouter(
    prefix="/roll", tags=["API roll"]
)


@router.post("/add")
async def api_add_roll(roll_data: SchemasRoll):
    return await RollDAO.add(
        length=roll_data.length,
        weight=roll_data.weight,
        added_date=roll_data.date_added,
        removed_date=roll_data.date_removed
    )


@router.delete("/delete/{id_roll}")
async def api_delete_roll(id_roll: int):
    async with async_session_maker() as session:
        # Находим рулон перед удалением
        query = select(Roll).where(Roll.id == id_roll)
        result = await session.execute(query)
        roll = result.scalar_one_or_none()

        if not roll:
            raise HTTPException(status_code=404, detail="Рулон не найден")

        await session.delete(roll)
        await session.commit()

        return {
            "id": roll.id,
            "length": roll.length,
            "weight": roll.weight,
            "added_date": roll.added_date,
            "removed_date": roll.removed_date
        }


@router.get("/all")
async def api_all_roll():
    return await RollDAO.find_all()


@router.get("/filter")
async def api_filter_roll(
        min_id: Optional[int] = Query(None, description="Минимальный идентификатор"),
        max_id: Optional[int] = Query(None, description="Максимальный идентификатор"),
        min_weight: Optional[int] = Query(None, description="Минимальный вес"),
        max_weight: Optional[int] = Query(None, description="Максимальный вес"),
        min_length: Optional[int] = Query(None, description="Минимальная длина"),
        max_length: Optional[int] = Query(None, description="Максимальная длина"),
        min_date_added: Optional[date] = Query(None, description="Минимальная дата добавления"),
        max_date_added: Optional[date] = Query(None, description="Максимальная дата добавления"),
        min_removed_date: Optional[date] = Query(None, description="Минимальная дата удаления"),
        max_removed_date: Optional[date] = Query(None, description="Максимальная дата удаления"),
):
    filters = RollFilter(
        min_id=min_id,
        max_id=max_id,
        min_weight=min_weight,
        max_weight=max_weight,
        min_length=min_length,
        max_length=max_length,
        min_date_added=min_date_added,
        max_date_added=max_date_added,
        min_removed_date=min_removed_date,
        max_removed_date=max_removed_date,
    )
    return await filter_roll(filters)


@router.get("/rolls/stats")
async def get_roll_stats(
        start_date: date = Query(..., description="Начальная дата для выборки"),
        end_date: date = Query(..., description="Конечная дата для выборки"),
):
    return await RollDAO.getting_statistics(start_date, end_date)