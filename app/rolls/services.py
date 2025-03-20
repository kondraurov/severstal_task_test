from app.rolls.dao import RollDAO
from app.exceptions import RollIdNotFound
from app.rolls.models import RollFilter


async def delete_roll(roll_id: int):
    roll = await RollDAO.find_by_id(roll_id)
    if roll is None:
        raise RollIdNotFound(f"Рулон с ID {roll_id} не найден.")
    return await RollDAO.delete(roll_id)


async def filter_roll(filters: RollFilter) -> list:
    filter_dict = filters.model_dump(exclude_unset=True)  # Заменил dict() на model_dump()

    if not filter_dict:
        raise ValueError("Укажите хотя бы один параметр фильтра")

    return await RollDAO.find_by_filter(**filter_dict)
