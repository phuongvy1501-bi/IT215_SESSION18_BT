from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import get_db
from schemas.registration import RegistrationCreate, RegistrationResponse
from crud import registration as crud_registration
from crud import student as crud_student
from crud import workshop as crud_workshop
from models.registration import Registration

router = APIRouter(prefix="/registrations", tags=["registrations"])

@router.post("/", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_workshop(reg_data: RegistrationCreate, db: Session = Depends(get_db)):
    # 1. Kiểm tra sinh viên
    db_student = crud_student.get_student(db, student_id=reg_data.student_id)
    if not db_student or db_student.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="Student not found or inactive")

    # 2. Kiểm tra workshop
    db_workshop = crud_workshop.get_workshop(db, workshop_id=reg_data.workshop_id)
    if not db_workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    
    if db_workshop.status != "OPEN":
        raise HTTPException(status_code=400, detail="Workshop is not open for registration")
    
    if db_workshop.start_time <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Workshop already started")

    # 3. Kiểm tra đăng ký trùng
    existing_reg = crud_registration.get_registration(db, student_id=reg_data.student_id, workshop_id=reg_data.workshop_id)
    if existing_reg:
        if existing_reg.status == "REGISTERED":
            raise HTTPException(status_code=400, detail="Student already registered for this workshop")
        else:
            # Nếu đã CANCELLED, có thể cập nhật lại trạng thái thành REGISTERED
            # Nhưng ở bài này ta có thể tạo mới hoặc update. Để đơn giản, update status
            pass # Sẽ xử lý ở dưới, có thể coi là đăng ký lại

    # 4. Kiểm tra sức chứa (giới hạn người)
    current_participants = crud_registration.count_workshop_participants(db, workshop_id=reg_data.workshop_id)
    if current_participants >= db_workshop.maximum_participants:
        raise HTTPException(status_code=400, detail="Workshop is full")

    # Thực hiện đăng ký
    if existing_reg and existing_reg.status == "CANCELLED":
        existing_reg.status = "REGISTERED"
        existing_reg.registered_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_reg)
        return existing_reg

    return crud_registration.create_registration(db=db, registration=reg_data)

@router.put("/{registration_id}", response_model=RegistrationResponse)
def cancel_registration(registration_id: int, db: Session = Depends(get_db)):
    db_reg = db.execute(
        select(Registration).where(Registration.id == registration_id)
    ).scalar_one_or_none()
    
    if not db_reg:
        raise HTTPException(status_code=404, detail="Registration not found")
        
    updated_reg = crud_registration.cancel_registration(db, registration_id=registration_id)
    return updated_reg

@router.delete("/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_registration(registration_id: int, db: Session = Depends(get_db)):
    """Soft delete (Cancel) the registration via DELETE method"""
    db_reg = crud_registration.cancel_registration(db, registration_id=registration_id)
    if not db_reg:
        raise HTTPException(status_code=404, detail="Registration not found")
    return
