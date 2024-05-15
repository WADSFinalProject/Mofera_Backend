from sqlalchemy.orm import Session
from models import *
from schemas import *

def get_wet_leaves_by_id(db: Session, wet_leaves_id: int):
    return db.query(WetLeaves).filter(WetLeaves.id == wet_leaves_id).first()

def get_wet_leaves(db: Session, skip: int = 0, limit: int = 10):
    return db.query(WetLeaves).offset(skip).limit(limit).all()

def create_wet_leaves (db: Session, wet_leaves: WetLeavesBase):
    db_wet_leaves = WetLeaves(retrieval_date=wet_leaves.retrieval_date, weight=wet_leaves.weight, centra_id=wet_leaves.centra_id)
    db.add(db_wet_leaves)
    db.commit()
    db.refresh(db_wet_leaves)
    return db_wet_leaves

def update_wet_leaves(db: Session, wet_leaves_id: int, wet_leaves: WetLeavesBase):
    db_wet_leaves = get_wet_leaves_by_id(db, wet_leaves_id)
    if db_wet_leaves:
        for key, value in wet_leaves.dict().items():
            setattr(db_wet_leaves, key, value)
        db.commit()
        db.refresh(db_wet_leaves)
    return db_wet_leaves

def delete_wet_leaves(db: Session, wet_leaves_id: int):
    db_wet_leaves = get_wet_leaves_by_id(db, wet_leaves_id)
    if db_wet_leaves:
        db.delete(db_wet_leaves)
        db.commit()
    return db_wet_leaves

