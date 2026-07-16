from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models.registration import Registration
from models.student import Student
from models.workshop import Workshop
from schemas.registration import RegistrationCreate

def get_registration(db: Session, student_id: int, workshop_id: int):
    return db.execute(
        select(Registration).where(
            Registration.student_id == student_id,
            Registration.workshop_id == workshop_id
        )
    ).scalar_one_or_none()

def count_workshop_participants(db: Session, workshop_id: int):
    # Chỉ đếm những người chưa CANCELLED
    result = db.execute(
        select(func.count(Registration.id)).where(
            Registration.workshop_id == workshop_id,
            Registration.status == "REGISTERED"
        )
    )
    return result.scalar()

def create_registration(db: Session, registration: RegistrationCreate):
    db_reg = Registration(
        student_id=registration.student_id,
        workshop_id=registration.workshop_id,
        status="REGISTERED"
    )
    db.add(db_reg)
    db.commit()
    db.refresh(db_reg)
    return db_reg

def cancel_registration(db: Session, registration_id: int):
    db_reg = db.execute(select(Registration).where(Registration.id == registration_id)).scalar_one_or_none()
    if db_reg:
        db_reg.status = "CANCELLED"
        db.commit()
        db.refresh(db_reg)
    return db_reg

def get_workshop_students(db: Session, workshop_id: int):
    # Trả về các sinh viên đăng ký hợp lệ
    stmt = (
        select(Student)
        .join(Registration, Student.id == Registration.student_id)
        .where(
            Registration.workshop_id == workshop_id,
            Registration.status == "REGISTERED",
            Student.status == "ACTIVE"
        )
        .distinct()
    )
    return db.execute(stmt).scalars().all()

def get_student_workshops(db: Session, student_id: int):
    # Trả về các workshop mà SV đăng ký hợp lệ
    stmt = (
        select(Workshop)
        .join(Registration, Workshop.id == Registration.workshop_id)
        .where(
            Registration.student_id == student_id,
            Registration.status == "REGISTERED"
        )
        .distinct()
    )
    return db.execute(stmt).scalars().all()
