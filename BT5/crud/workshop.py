from sqlalchemy.orm import Session
from sqlalchemy import select
from models.workshop import Workshop
from schemas.workshop import WorkshopCreate

def get_workshop(db: Session, workshop_id: int):
    return db.execute(select(Workshop).where(Workshop.id == workshop_id)).scalar_one_or_none()

def get_workshops(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(Workshop).offset(skip).limit(limit)).scalars().all()

def create_workshop(db: Session, workshop: WorkshopCreate):
    db_workshop = Workshop(**workshop.model_dump())
    db.add(db_workshop)
    db.commit()
    db.refresh(db_workshop)
    return db_workshop
