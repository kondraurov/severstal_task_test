from pydantic import BaseModel, Field, field_validator, ValidationInfo
from datetime import date
from typing import Optional


class SchemasRoll(BaseModel):
    length: float = Field(..., ge=0, description="Длина рулона")
    weight: float = Field(..., ge=0, description="Вес рулона")
    date_added: Optional[date] = Field(None, description="Дата добавления")
    date_removed: Optional[date] = Field(None, description="Дата удаления")

    @field_validator("date_removed")
    @classmethod
    def validate_dates(cls, date_removed: Optional[date], values: ValidationInfo):
        date_added = values.data.get("date_added")
        if date_removed and date_added and date_removed < date_added:
            raise ValueError("Дата удаления не может быть раньше даты добавления")
        return date_removed