from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List

from core.database import get_db
from models.course import Course
from models.student import Student
from models.enrollment import Enrollment
from schemas.course import CourseStudentsResponse

router = APIRouter()

@router.get("/courses/{course_id}/students", response_model=CourseStudentsResponse)
def get_course_students(course_id: int, db: Session = Depends(get_db)):
    # 1. Kiểm tra khóa học tồn tại
    course = db.execute(select(Course).where(Course.id == course_id)).scalar_one_or_none()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Course not found"
        )
    
    # 2. Sử dụng JOIN để lấy danh sách sinh viên theo yêu cầu
    # Điều kiện: Course ID = course_id, Enrollment status (STUDYING, COMPLETED), Student status (ACTIVE)
    # Loại bỏ trùng bằng distinct, sắp xếp theo tên
    stmt = (
        select(Student)
        .join(Enrollment, Student.id == Enrollment.student_id)
        .where(
            Enrollment.course_id == course_id,
            Enrollment.status.in_(["STUDYING", "COMPLETED"]),
            Student.status == "ACTIVE"
        )
        .distinct()
        .order_by(Student.full_name.asc())
    )
    
    result = db.execute(stmt)
    students = result.scalars().all()
    
    return CourseStudentsResponse(
        course_id=course.id,
        course_name=course.name,
        total_students=len(students),
        students=students
    )
