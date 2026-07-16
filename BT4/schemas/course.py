from pydantic import BaseModel
from typing import List
from .student import StudentResponse

class CourseStudentsResponse(BaseModel):
    course_id: int
    course_name: str
    total_students: int
    students: List[StudentResponse]
