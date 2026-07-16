from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from .base import Base
from typing import List

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE") # ACTIVE, INACTIVE

    # Relationship
    registrations: Mapped[List["Registration"]] = relationship(back_populates="student")
