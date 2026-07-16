from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from schemas.workshop import WorkshopCreate, WorkshopResponse, WorkshopWithStudents
from crud import workshop as crud_workshop
from crud import registration as crud_registration

router = APIRouter(prefix="/workshops", tags=["workshops"])

@router.post("/", response_model=WorkshopResponse, status_code=status.HTTP_201_CREATED)
def create_workshop(workshop: WorkshopCreate, db: Session = Depends(get_db)):
    return crud_workshop.create_workshop(db=db, workshop=workshop)

@router.get("/", response_model=List[WorkshopResponse])
def read_workshops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    workshops = crud_workshop.get_workshops(db, skip=skip, limit=limit)
    return workshops

@router.get("/{workshop_id}", response_model=WorkshopResponse)
def read_workshop(workshop_id: int, db: Session = Depends(get_db)):
    db_workshop = crud_workshop.get_workshop(db, workshop_id=workshop_id)
    if not db_workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return db_workshop

@router.get("/{workshop_id}/students", response_model=WorkshopWithStudents)
def get_workshop_students(workshop_id: int, db: Session = Depends(get_db)):
    db_workshop = crud_workshop.get_workshop(db, workshop_id=workshop_id)
    if not db_workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    
    students = crud_registration.get_workshop_students(db, workshop_id=workshop_id)
    
    workshop_data = WorkshopResponse.model_validate(db_workshop).model_dump()
    return WorkshopWithStudents(**workshop_data, students=students)
