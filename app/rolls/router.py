from fastapi import APIRouter, Query, HTTPException
from app.rolls.models import RollFilter
from app.rolls.schemas import SchemasRoll
from app.rolls.dao import RollDAO
from app.rolls.services import filter_roll, delete_roll
from typing import Optional
from datetime import date, datetime

router = APIRouter(
    prefix="/roll", tags=["API roll"]
)


@router.post("/add")
async def api_add_roll(roll_data: SchemasRoll):
    # Возможно, тут необходимо добавить обработку ошибок
    try:
        return await RollDAO.add(
            length=roll_data.length,
            weight=roll_data.weight,
            date_added=roll_data.date_added,
            date_removed=roll_data.date_removed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding roll: {e}")


@router.delete("/delete/{id_roll}")
async def api_delete_roll(id_roll: int):
    try:
        return await delete_roll(id_roll)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Roll with ID {id_roll} not found: {e}")


@router.get("/all")
async def api_all_roll():
    return await RollDAO.find_all()


@router.get("/filter")
async def api_filter_roll(
        min_id: Optional[int] = Query(None, description="Минимальный id"),
        max_id: Optional[int] = Query(None, description="Максимальный id"),
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
        start_date: datetime = Query(..., description="Начальная дата периода"),
        end_date: datetime = Query(..., description="Конечная дата периода"),
):
    return await RollDAO.getting_statistics(start_date, end_date)
