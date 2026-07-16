from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime
from .base import Base

class Registration(Base):
    __tablename__ = "registrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    workshop_id: Mapped[int] = mapped_column(ForeignKey("workshops.id"), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(50), default="REGISTERED") # REGISTERED, CANCELLED

    # Relationships
    student: Mapped["Student"] = relationship(back_populates="registrations")
    workshop: Mapped["Workshop"] = relationship(back_populates="registrations")
