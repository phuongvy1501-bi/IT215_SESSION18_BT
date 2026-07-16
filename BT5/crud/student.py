from sqlalchemy.orm import Session
from sqlalchemy import select
from models.student import Student
from schemas.student import StudentCreate

def get_student(db: Session, student_id: int):
    return db.execute(select(Student).where(Student.id == student_id)).scalar_one_or_none()

def get_student_by_email_or_code(db: Session, email: str, student_code: str):
    return db.execute(
        select(Student).where(
            (Student.email == email) | (Student.student_code == student_code)
        )
    ).scalar_one_or_none()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(Student).offset(skip).limit(limit)).scalars().all()

def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student
