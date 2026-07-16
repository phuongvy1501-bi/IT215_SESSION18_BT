from pydantic import BaseModel
from datetime import datetime
from .student import StudentResponse
from .workshop import WorkshopResponse
from typing import List

class RegistrationCreate(BaseModel):
    student_id: int
    workshop_id: int

class RegistrationResponse(BaseModel):
    id: int
    student_id: int
    workshop_id: int
    registered_at: datetime
    status: str

    class Config:
        from_attributes = True

class StudentWorkshopsResponse(StudentResponse):
    workshops: List[WorkshopResponse] = []
