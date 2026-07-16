from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from .base import Base

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE") # ACTIVE, INACTIVE

    # Relationship
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="student")
