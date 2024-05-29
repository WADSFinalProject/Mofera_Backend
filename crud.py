from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import models
import schemas
from datetime import date
from fastapi import HTTPException

def get_wet_leaves_by_id(db: Session, wet_leaves_id: int):
    return db.query(models.Wet).filter(models.Wet.id == wet_leaves_id).first()

def get_dry_leaves_by_id(db: Session, dry_leaves_id: int):
    return db.query(models.Dry).filter(models.Dry.id == dry_leaves_id).first()

def get_flour_by_id(db: Session, flour_id: int):
    return db.query(models.Flour).filter(models.Flour.id == flour_id).first()

def get_shipping_by_id(db: Session, shipping_id: int):
    return db.query(models.Shipping).filter(models.Shipping.id == shipping_id).first()

def get_checkpoint_by_id(db: Session, checkpoint_id: int):
    return db.query(models.CheckpointData).filter(models.CheckpointData.id == checkpoint_id).first()

def get_centra_notifications_by_id(db: Session, centra_notif_id: int):
    return db.query(models.CentraNotification).filter(models.CentraNotification.id == centra_notif_id).first()

def get_reception_packages_by_id(db: Session, reception_packages_id: int):
    return db.query(models.ReceptionPackage).filter(models.ReceptionPackage.id == reception_packages_id).first()

def get_checkpoints(db: Session, skip: int = 0, limit: int = 10, date_filter: date = None, before: bool = None, after: bool = None):
    query = db.query(models.CheckpointData)
    if date_filter:
        if before:
            query = query.filter(models.CheckpointData.arrival_date < date_filter)
        elif after:
            query = query.filter(models.CheckpointData.arrival_date > date_filter)
        else:
            query = query.filter(models.CheckpointData.arrival_date == date_filter)
    return query.offset(skip).limit(limit).all()

def update_checkpoint(db: Session, checkpoint_id: int, checkpoint: schemas.CheckpointDataRecord):
    query = db.query(models.CheckpointData).filter(models.CheckpointData.id == checkpoint_id)
    if not query:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    query.update(**checkpoint.model_dump())
    db.commit()
    db.refresh(query)
    return query


def get_wet_leaves(db: Session, skip: int = 0, limit: int = 10, date_filter: date = None, before: bool = None, after: bool = None):
    query = db.query(models.Wet)
    if date_filter:
        if before:
            query = query.filter(models.Collection.retrieval_date < date_filter)
        elif after:
            query = query.filter(models.Collection.retrieval_date > date_filter)
        else:
            query = query.filter(models.Collection.retrieval_date == date_filter)
    return query.offset(skip).limit(limit).all()

def get_dry_leaves(db: Session, skip: int = 0, limit: int = 10, date_filter: date = None, before: bool = None, after: bool = None):
    query = db.query(models.Dry)
    if date_filter:
        if before:
            query = query.filter(models.Dry.dried_date < date_filter)
        elif after:
            query = query.filter(models.Dry.dried_date > date_filter)
        else:
            query = query.filter(models.Dry.dried_date == date_filter)
    return query.offset(skip).limit(limit).all()

def get_flour(db: Session, skip: int = 0, limit: int = 10, date_filter: date = None, before: bool = None, after: bool = None):
    query = db.query(models.Flour)
    if date_filter:
        if before:
            query = query.filter(models.Flour.finish_time < date_filter)
        elif after:
            query = query.filter(models.Flour.finish_time > date_filter)
        else:
            query = query.filter(models.Flour.finish_time == date_filter)
    return query.offset(skip).limit(limit).all()

def wash_wet_leaves(db: Session, id: int, date: schemas.DateRecord):
    query = db.query(models.Wet).filter(models.Wet.id == id).update({models.Wet.washed_date: date.date})
    db.commit()
    return query

def dry_wet_leaves(db: Session, id: int, date: schemas.DateRecord):
    query = db.query(models.Wet).filter(models.Wet.id == id).update({models.Wet.dried_date: date.date})
    db.commit()
    return query

def flour_dry_leaves(db: Session, id: int, date: schemas.DateRecord):
    query = db.query(models.Dry).filter(models.Dry.id == id).update({models.Dry.floured_date: date.date})
    db.commit()
    return query

def get_shipping(db: Session, skip: int = 0, limit: int = 10, date_filter: date = None, before: bool = None, after: bool = None):
    query = db.query(models.Shipping)
    if date_filter:
        if before:
            query = query.filter(models.Shipping.departure_date < date_filter)
        elif after:
            query = query.filter(models.Shipping.departure_date > date_filter)
        else:
            query = query.filter(models.Shipping.departure_date == date_filter)
    return query.offset(skip).limit(limit).all()

def get_centra_notifications(db: Session, skip: int = 0, limit: int = 10, date_filter: date = None, before: bool = None, after: bool = None):
    query = db.query(models.CentraNotification)
    if date_filter:
        if before:
            query = query.filter(models.CentraNotification.date < date_filter)
        elif after:
            query = query.filter(models.CentraNotification.date > date_filter)
        else:
            query = query.filter(models.CentraNotification.date == date_filter)
    return query.offset(skip).limit(limit).all()

def get_reception_packages(db: Session, skip: int = 0, limit: int = 10, date_filter: date = None, before: bool = None, after: bool = None):
    query = db.query(models.ReceptionPackage)
    if date_filter:
        if before:
            query = query.filter(models.ReceptionPackage.receival_date < date_filter)
        elif after:
            query = query.filter(models.ReceptionPackage.receival_date > date_filter)
        else:
            query = query.filter(models.ReceptionPackage.receival_date == date_filter)
    return query.offset(skip).limit(limit).all()

def create_wet_leaves(db: Session, wet_leaves: schemas.WetLeavesRecord):
    db_wet_leaves = models.Wet(retrieval_date=wet_leaves.retrieval_date, weight=wet_leaves.weight)
    db.add(db_wet_leaves)
    db.commit()
    db.refresh(db_wet_leaves)
    return db_wet_leaves

def create_dry_leaves(db: Session, dry_leaves: schemas.DryLeavesRecord):
    db_dry_leaves = models.Dry(dried_date=dry_leaves.dried_date, weight=dry_leaves.weight)
    db.add(db_dry_leaves)
    db.commit()
    db.refresh(db_dry_leaves)
    return db_dry_leaves

def create_flour(db: Session, flour: schemas.FlourRecord):
    db_flour = models.Flour(**flour.model_dump())
    db.add(db_flour)
    db.commit()
    db.refresh(db_flour)
    return db_flour

def create_shipping(db: Session, shipping: schemas.ShippingDepature):
    db_shipping = models.Shipping(departure_date=shipping.departure_date, expedition_id=shipping.expedition_id)
    db.add(db_shipping)
    db.commit()
    db.refresh(db_shipping)
    return db_shipping

def create_checkpoint(db: Session, checkpoint: schemas.CheckpointDataRecord):
    db_checkpoint = models.CheckpointData(**checkpoint.model_dump())
    db.add(db_checkpoint)
    db.commit()
    db.refresh(db_checkpoint)
    return db_checkpoint

def create_centra_notifications(db: Session, centra_notif: schemas.CentraNotification):
    db_centra_notif = models.CentraNotification(message=centra_notif.message, user_id=centra_notif.user_id)
    db.add(db_centra_notif)
    db.commit()
    db.refresh(db_centra_notif)
    return db_centra_notif

def create_reception_packages(db: Session, reception_packages: schemas.ReceptionPackageRecord):
    db_reception_packages = models.ReceptionPackage(**reception_packages.model_dump())
    db.add(db_reception_packages)
    db.commit()
    db.refresh(db_reception_packages)
    return db_reception_packages

def update_wet_leaves(db: Session, wet_leaves_id: int, wet_leaves: schemas.WetLeavesBase):
    db_wet_leaves = get_wet_leaves_by_id(db, wet_leaves_id)
    if db_wet_leaves:
        for key, value in wet_leaves.model_dump().items():
            setattr(db_wet_leaves, key, value)
        db.commit()
        db.refresh(db_wet_leaves)
    return db_wet_leaves

def update_dry_leaves(db: Session, dry_leaves_id: int, dry_leaves: schemas.DryLeavesBase):
    db_dry_leaves = get_dry_leaves_by_id(db, dry_leaves_id)
    if db_dry_leaves:
        for key, value in dry_leaves.model_dump().items():
            setattr(db_dry_leaves, key, value)
        db.commit()
        db.refresh(db_dry_leaves)
    return db_dry_leaves

def update_flour(db: Session, flour_id: int, flour: schemas.FlourBase):
    db_flour = get_flour_by_id(db, flour_id)
    if db_flour:
        for key, value in flour.model_dump().items():
            setattr(db_flour, key, value)
        db.commit()
        db.refresh(db_flour)
    return db_flour

def update_shipping(db: Session, shipping_id: int, shipping: schemas.ShippingDataRecord):
    db_shipping = get_shipping_by_id(db, shipping_id)
    if db_shipping:
        for key, value in shipping.model_dump().items():
            setattr(db_shipping, key, value)
        db.commit()
        db.refresh(db_shipping)
    return db_shipping

def update_checkpoint(db: Session, checkpoint_id: int, checkpoint: schemas.CheckpointDataRecord):
    db_checkpoint = get_checkpoint_by_id(db, checkpoint_id)
    if not db_checkpoint:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    for key, value in checkpoint.model_dump().items():
        setattr(db_checkpoint, key, value)
    db.commit()
    db.refresh(db_checkpoint)
    return db_checkpoint

def update_centra_notifications(db: Session, centra_notif_id: int, centra_notif: schemas.CentraNotification):
    db_centra_notif = get_centra_notifications_by_id(db, centra_notif_id)
    if db_centra_notif:
        for key, value in centra_notif.model_dump().items():
            setattr(db_centra_notif, key, value)
        db.commit()
        db.refresh(db_centra_notif)
    return db_centra_notif

def update_reception_packages(db: Session, reception_packages_id: int, reception_packages: schemas.ReceptionPackage):
    db_reception_packages = get_reception_packages_by_id(db, reception_packages_id)
    if db_reception_packages:
        for key, value in reception_packages.model_dump().items():
            setattr(db_reception_packages, key, value)
        db.commit()
        db.refresh(db_reception_packages)
    return db_reception_packages

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
    if not db_checkpoint:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    db.delete(db_checkpoint)
    db.commit()
    return db_checkpoint

def delete_centra_notifications(db: Session, centra_notif_id: int):
    db_centra_notif = get_centra_notifications_by_id(db, centra_notif_id)
    if db_centra_notif:
        db.delete(db_centra_notif)
        db.commit()
    return db_centra_notif

def delete_reception_packages(db: Session, reception_packages_id: int):
    db_reception_packages = get_reception_packages_by_id(db, reception_packages_id)
    if db_reception_packages:
        db.delete(db_reception_packages)
        db.commit()
    return db_reception_packages
