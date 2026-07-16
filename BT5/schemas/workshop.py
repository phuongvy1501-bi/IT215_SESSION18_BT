from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .student import StudentResponse

class WorkshopCreate(BaseModel):
    title: str
    description: Optional[str] = None
    maximum_participants: int
    status: Optional[str] = "OPEN"
    start_time: datetime

class WorkshopResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    maximum_participants: int
    status: str
    start_time: datetime

    class Config:
        from_attributes = True

class WorkshopWithStudents(WorkshopResponse):
    students: List[StudentResponse] = []
