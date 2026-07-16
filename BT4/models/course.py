from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from .base import Base

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="OPEN") # OPEN, CLOSED

    # Relationship
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="course")
