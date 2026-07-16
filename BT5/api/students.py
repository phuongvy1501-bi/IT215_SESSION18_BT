from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from schemas.student import StudentCreate, StudentResponse
from schemas.registration import StudentWorkshopsResponse
from crud import student as crud_student
from crud import registration as crud_registration

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = crud_student.get_student_by_email_or_code(db, email=student.email, student_code=student.student_code)
    if db_student:
        raise HTTPException(status_code=400, detail="Email or Student Code already registered")
    return crud_student.create_student(db=db, student=student)

@router.get("/", response_model=List[StudentResponse])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud_student.get_students(db, skip=skip, limit=limit)
    return students

@router.get("/{student_id}/workshops", response_model=StudentWorkshopsResponse)
def get_student_workshops(student_id: int, db: Session = Depends(get_db)):
    db_student = crud_student.get_student(db, student_id=student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    workshops = crud_registration.get_student_workshops(db, student_id=student_id)
    
    # Map data cho response nested
    student_data = StudentResponse.model_validate(db_student).model_dump()
    return StudentWorkshopsResponse(**student_data, workshops=workshops)
