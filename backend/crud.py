from sqlalchemy.orm import Session
from models import *
from schemas import *

def get_wet_leaves_by_id(db: Session, wet_leaves_id: int):
    return db.query(WetLeaves).filter(WetLeaves.id == wet_leaves_id).first()

def get_dry_leaves_by_id(db: Session, dry_leaves_id: int):
    return db.query(DryLeaves).filter(DryLeaves.id == dry_leaves_id).first()
def get_flour_by_id(db: Session, flour_id: int):
    return db.query(Flour).filter(Flour.id == flour_id).first()

def get_shipping_by_id(db: Session, shipping_id: int):
    return db.query(Shipping).filter(Shipping.id == shipping_id).first()

def get_checkpoint_by_id(db: Session, checkpoint_id: int):
    return db.query(CheckpointData).filter(CheckpointData.id == checkpoint_id).first()

def get_checkpoints(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CheckpointData).offset(skip).limit(limit).all()

def get_wet_leaves(db: Session, skip: int = 0, limit: int = 10):
    return db.query(WetLeaves).offset(skip).limit(limit).all()

def get_dry_leaves(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DryLeaves).offset(skip).limit(limit).all()

def get_flour(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Flour).offset(skip).limit(limit).all()

def get_shipping(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Shipping).offset(skip).limit(limit).all()

def create_wet_leaves (db: Session, wet_leaves: WetLeavesRecord):
    db_wet_leaves = WetLeaves(retrieval_date=wet_leaves.retrieval_date, weight=wet_leaves.weight)
    db.add(db_wet_leaves)
    db.commit()
    db.refresh(db_wet_leaves)
    return db_wet_leaves

def create_dry_leaves (db: Session, dry_leaves: DryLeavesRecord):
    db_dry_leaves = DryLeaves(exp_date=dry_leaves.exp_date, weight=dry_leaves.weight)
    db.add(db_dry_leaves)
    db.commit()
    db.refresh(db_dry_leaves)
    return db_dry_leaves

def create_flour (db: Session, flour: FlourRecord):
    db_flour = Flour(finish_time=flour.finish_time, weight=flour.weight)
    db.add(db_flour)
    db.commit()
    db.refresh(db_flour)
    return db_flour

def create_shipping (db: Session, shipping: ShippingDepature):
    db_shipping = Shipping(departure_date=shipping.departure_date, expedition_id=shipping.expedition_id)
    db.add(db_shipping)
    db.commit()
    db.refresh(db_shipping)
    return db_shipping

def create_checkpoint (db: Session, checkpoint: CheckpointData):
    db_checkpoint = CheckpointData(**checkpoint.dict())
    db.add(db_checkpoint)
    db.commit()
    db.refresh(db_checkpoint)
    return db_checkpoint

def update_wet_leaves(db: Session, wet_leaves_id: int, wet_leaves: WetLeavesBase):
    db_wet_leaves = get_wet_leaves_by_id(db, wet_leaves_id)
    if db_wet_leaves:
        for key, value in wet_leaves.dict().items():
            setattr(db_wet_leaves, key, value)
        db.commit()
        db.refresh(db_wet_leaves)
    return db_wet_leaves

def update_dry_leaves(db: Session, dry_leaves_id: int, dry_leaves: DryLeavesBase):
    db_dry_leaves = get_dry_leaves_by_id(db, dry_leaves_id)
    if db_dry_leaves:
        for key, value in dry_leaves.dict().items():
            setattr(db_dry_leaves, key, value)
        db.commit()
        db.refresh(db_dry_leaves)
    return db_dry_leaves

def update_flour(db: Session, flour_id: int, flour: FlourBase):
    db_flour = get_flour_by_id(db, flour_id)
    if db_flour:
        for key, value in flour.dict().items():
            setattr(db_flour, key, value)
        db.commit()
        db.refresh(db_flour)
    return db_flour

def update_shipping(db: Session, shipping_id: int, shipping: ShippingDataRecord):
    db_shipping = get_shipping_by_id(db, shipping_id)
    if db_shipping:
        for key, value in shipping.dict().items():
            setattr(db_shipping, key, value)
        db.commit()
        db.refresh(db_shipping)
    return db_shipping

def update_checkpoint(db: Session, checkpoint_id: int, checkpoint: CheckpointDataRecord):
    db_checkpoint = get_checkpoint_by_id(db, checkpoint_id)
    if db_checkpoint:
        for key, value in checkpoint.dict().items():
            setattr(db_checkpoint, key, value)
        db.commit()
        db.refresh(db_checkpoint)
    return db_checkpoint

def delete_wet_leaves(db: Session, wet_leaves_id: int):
    db_wet_leaves = get_wet_leaves_by_id(db, wet_leaves_id)
    if db_wet_leaves:
        db.delete(db_wet_leaves)
        db.commit()
    return db_wet_leaves

def delete_dry_leaves(db: Session, dry_leaves_id: int):
    db_dry_leaves = get_dry_leaves_by_id(db, dry_leaves_id)
    if db_dry_leaves:
        db.delete(db_dry_leaves)
        db.commit()
    return db_dry_leaves

def delete_flour(db: Session, flour_id: int):
    db_flour = get_flour_by_id(db, flour_id)
    if db_flour:
        db.delete(db_flour)
        db.commit()
    return db_flour

def delete_shipping(db: Session, shipping_id: int):
    db_shipping = get_shipping_by_id(db, shipping_id)
    if db_shipping:
        db.delete(db_shipping)
        db.commit()
    return db_shipping

def delete_checkpoint(db: Session, checkpoint_id: int):
    db_checkpoint = get_checkpoint_by_id(db, checkpoint_id)
    if db_checkpoint:
        db.delete(db_checkpoint)
        db.commit()
    return db_checkpoint



