from pydantic import BaseModel, EmailStr
from typing import Optional

class StudentCreate(BaseModel):
    student_code: str
    full_name: str
    email: EmailStr
    status: Optional[str] = "ACTIVE"

class StudentResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    email: EmailStr
    status: str

    class Config:
        from_attributes = True
