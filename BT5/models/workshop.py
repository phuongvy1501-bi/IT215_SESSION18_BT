from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime
from datetime import datetime
from .base import Base
from typing import List

class Workshop(Base):
    __tablename__ = "workshops"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    maximum_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="OPEN") # OPEN, CLOSED, CANCELLED
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationship
    registrations: Mapped[List["Registration"]] = relationship(back_populates="workshop")
