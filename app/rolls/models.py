from datetime import datetime
from sqlalchemy import Integer, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import date

class Roll(Base):
    __tablename__ = "rolls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    length: Mapped[float] = mapped_column(Float, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    added_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp())
    removed_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

class RollFilter(BaseModel):
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    min_weight: Optional[int] = None
    max_weight: Optional[int] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    added_from: Optional[date] = None
    min_date_added: Optional[date] = None
    min_removed_date: Optional[date] = None
    max_removed_date: Optional[date] = None