from sqlalchemy.orm import Session, Query
from sqlalchemy import and_, or_, func
from sqlalchemy.sql import extract
import models
import schemas
import auth
import datetime
from datetime import date, timedelta
from fastapi import HTTPException
from typing import Optional, Union

def get_centra_by_id(db: Session, centra_id: int):
    return db.query(models.Centra).filter(models.Centra.id == centra_id).first()

def get_wet_leaves_by_id(db: Session, wet_leaves_id: int):
    return db.query(models.Wet).filter(models.Wet.id == wet_leaves_id).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()

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

def get_package_by_id(db: Session, package_id: int):
    return db.query(models.PackageData).filter(models.PackageData.id == package_id).first()

def get_reception_packages_by_id(db: Session, reception_packages_id: int):
    return db.query(models.ReceptionPackage).filter(models.ReceptionPackage.id == reception_packages_id).first()

def get_checkpoints(db: Session, year: int = 0, month: int = 0, day: int = 0, filter: str = "", skip: int = 0, limit: int = 20):
    query = db.query(models.CheckpointData)

    if year and month and day:
        if filter == "w":
            # Calculate start of week
            start_date = date(year, month, day) - timedelta(days=date(year, month, day).weekday())
            # Ensure the end date is the start date + 6 days to cover the whole week
            end_date = start_date + timedelta(days=6)
            query = query.filter(func.DATE(models.CheckpointData.arrival_datetime).between(start_date, end_date))
        else: query = query.filter(func.DATE(models.CheckpointData.arrival_datetime) == date(year, month, day))

    elif year:
        query = query.filter(extract("year", models.CheckpointData.arrival_datetime) == year)

        if month:
            query = query.filter(extract("month", models.CheckpointData.arrival_datetime) == month)

    if skip:
        query = query.offset(skip)
    
    if limit:
        query = query.limit(limit)  

    return query.all()

# def get_checkpoints(db: Session, skip: int = 0, limit: int = 10, date_filter: date = None, before: bool = None, after: bool = None):
#     query = db.query(models.CheckpointData)
#     if date_filter:
#         if before:
#             query = query.filter(models.CheckpointData.arrival_datetime < date_filter)
#         elif after:
#             query = query.filter(models.CheckpointData.arrival_datetime > date_filter)
#         else:
#             query = query.filter(models.CheckpointData.arrival_datetime == date_filter)
#     return query.offset(skip).limit(limit).all()
def get_checkpoint_summary(db: Session, shipping_id: int = 0):
    today = date.today()
    query = db.query(models.CheckpointData)
    
    if shipping_id:
        query = query.filter(models.CheckpointData.shipping_id == shipping_id)

    total = len(query.all())
    monthly = len(get_checkpoints(db=db, year=today.year, month=today.month))/today.day
    today = len(get_checkpoints(db=db, year=today.year, month=today.month, day=today.day))
    
    return {"total": total, "monthly": monthly, "today": today}


def get_users(db: Session, skip: int = 0, limit: int = 10000):
    return db.query(models.Users).offset(skip).limit(limit).all()

def update_user(db: Session, user: models.Users, user_update: schemas.UserUpdate):
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: models.Users):
    db.delete(user)
    db.commit()

def get_centra(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Centra).offset(skip).limit(limit).all()

def update_checkpoint(db: Session, id: int):

    update_package_status_by_id(db, id, 2)
    return

def filter_by_centra_id(query: Query, model: models, centra_id: int):
    if centra_id is not None:
        query = query.filter(model.centra_id == centra_id)
    return query

def get_collection(db: Session, centra_id: int, skip: int = 0, limit: int = 10, date_filter: datetime = None, before: bool = None, after: bool = None):
    query = db.query(models.Collection)
    if date_filter:
        if before:
            query = query.filter(models.Collection.retrieval_datetime < date_filter)
        elif after:
            query = query.filter(models.Collection.retrieval_datetime > date_filter)
        else:
            query = query.filter(models.Collection.retrieval_datetime == date_filter)

    query = filter_by_centra_id(query, models.Collection, centra_id)
    return query.offset(skip).limit(limit).all()

def get_wet_leaves(db: Session, centra_id: int = 0, skip: int = 0, limit: int = 20, year: int = 0, month: int = 0, day: int = 0, filter: str = ""):
    query = db.query(models.Wet)
    if year and month and day:
        if filter == "w":
            query = query.filter(models.Wet.retrieval_date.between(date(year, month, day)-timedelta(days=date(year, month, day).isoweekday()-1), date(year, month, day) + timedelta(days=7-date(year, month, day).isoweekday())))
        else: query = query.filter(models.Wet.retrieval_date == date(year, month, day))

    elif year:
        query = query.filter(extract("year", models.Wet.retrieval_date) == year)
    
        if month:
            query = query.filter(extract("month", models.Wet.retrieval_date) == month)

    if centra_id: query = filter_by_centra_id(query, models.Wet, centra_id)

    if skip:
        query = query.offset(skip)
    
    if limit:
        query = query.limit(limit)        
    
    return query.all()

def get_wet_summary(db: Session, centra_id: int = 0):
    today = date.today()
    query = db.query(models.Wet)
    
    if centra_id:
        query = query.filter(models.Wet.centra_id == centra_id)

    total = sum(wet.weight for wet in query.all())
    if total is None: total = 0
    monthly = sum(wet.weight for wet in get_wet_leaves(db=db, centra_id=centra_id, year=today.year, month=today.month))/today.day
    if monthly is None: monthly = 0
    today = sum(wet.weight for wet in get_wet_leaves(db=db, centra_id=centra_id, year=today.year, month=today.month, day=today.day))
    if today is None: today = 0
    
    return {"total": total, "monthly": monthly, "today": today}

    
def get_washed_wet_leaves(db: Session, centra_id: int = 0, skip: int = 0, limit: int = 10, date_filter: date = None, before: bool = None, after: bool = None):
    query = db.query(models.Wet).filter(models.Wet.washed_datetime <= datetime.datetime.now())
    if date_filter:
        if before:
            query = query.filter(models.Wet.retrieval_date < date_filter)
        elif after:
            query = query.filter(models.Wet.retrieval_date > date_filter)
        else:
            query = query.filter(models.Wet.retrieval_date == date_filter)
    
    if centra_id: query = filter_by_centra_id(query, models.Wet, centra_id)
    return query.offset(skip).limit(limit).all()

def get_dry_leaves(db: Session, centra_id: int = 0, skip: int = 0, limit: int = 10, date_filter: date = None, before: bool = None, after: bool = None, between: bool = None):
    query = db.query(models.Dry)
    if date_filter:
        if before:
            query = query.filter(models.Dry.floured_datetime < date_filter)
        elif after:
            query = query.filter(models.Dry.floured_datetime > date_filter)
        else:
            query = query.filter(models.Dry.floured_datetime == date_filter)
    
    if centra_id:
        query = filter_by_centra_id(query, models.Dry, centra_id)
    return query.offset(skip).limit(limit).all()

def get_dry_leaves_by_dried_date(db: Session, centra_id: int=0, skip: int = 0, limit: int = 20, year: int = 0, month: int = 0, day: int = 0, filter: str = ""):
    query = db.query(models.Dry)
    if year and month and day:
        if filter == "w":
            query = query.filter(models.Dry.dried_date.between(date(year, month, day)-timedelta(days=date(year, month, day).isoweekday()-1), date(year, month, day) + timedelta(days=7-date(year, month, day).isoweekday())))
        else: query = query.filter(models.Dry.dried_date == date(year, month, day))

    elif year:
        query = query.filter(extract("year", models.Dry.dried_date) == year)
    
        if month:
            query = query.filter(extract("month", models.Dry.dried_date) == month)

    if centra_id: query = filter_by_centra_id(query, models.Dry, centra_id)

    if skip:
        query = query.offset(skip)
    
    if limit:
        query = query.limit(limit)        
    
    return query.all()

def get_dry_leaves_mobile(db: Session, date_origin:date, interval: str, centra_id: int=0, skip: int = 0, limit: int = 10):
    query = db.query(models.Dry)
    query = query.filter(models.Dry.dried_date >= date_origin)
    date_range = timedelta(days = 0)
    if interval == "1d":
        date_range = timedelta(days=1)
    elif interval == "3d":
        date_range = timedelta(days=3)
    elif interval == "7d":
        date_range = timedelta(days=7)
    
    query = query.filter(models.Dry.dried_date <= date_range+date_origin)
    if centra_id: query = filter_by_centra_id(query, models.Dry, centra_id)
    return query.offset(skip).limit(limit).all()

def get_dry_summary(db: Session, centra_id: int = 0):
    today = date.today()
    query = db.query(models.Dry)
    
    if centra_id:
        query = query.filter(models.Dry.centra_id == centra_id)

    total = sum(dry.weight for dry in query.all())
    if total is None: total = 0
    monthly = sum(dry.weight for dry in get_dry_leaves_by_dried_date(db=db, centra_id=centra_id, year=today.year, month=today.month))/today.day
    if monthly is None: monthly = 0
    today = sum(dry.weight for dry in get_dry_leaves_by_dried_date(db=db, centra_id=centra_id, year=today.year, month=today.month, day=today.day))
    if today is None: today = 0
    return {"total": total, "monthly": monthly, "today": today}

def get_flour(db: Session, centra_id: int = 0, skip: int = 0, limit: int = 10, date_filter: date = None, before: bool = None, after: bool = None):
    query = db.query(models.Flour)
    if date_filter:
        if before:
            query = query.filter(models.Flour.finish_time < date_filter)
        elif after:
            query = query.filter(models.Flour.finish_time > date_filter)
        else:
            query = query.filter(models.Flour.finish_time == date_filter)
    if centra_id: query = filter_by_centra_id(query, models.Flour, centra_id)
    return query.offset(skip).limit(limit).all()

def get_flour_by_floured_date(db: Session, centra_id: int = 0, skip: int = 0, limit: int = 20, year: int = 0, month: int = 0, day: int = 0, filter: str = ""):
    query = db.query(models.Flour)
    if year and month and day:
        if filter == "w":
            query = query.filter(models.Flour.floured_date.between(date(year, month, day)-timedelta(days=date(year, month, day).isoweekday()-1), date(year, month, day) + timedelta(days=7-date(year, month, day).isoweekday())))
        else: query = query.filter(models.Flour.floured_date == date(year, month, day))

    elif year:
        query = query.filter(extract("year", models.Flour.floured_date) == year)
    
        if month:
            query = query.filter(extract("month", models.Flour.floured_date) == month)

    if centra_id: query = query.filter(models.Flour.centra_id == centra_id)

    if skip:
        query = query.offset(skip)
    
    if limit:
        query = query.limit(limit)        
    

    return query.all()

def get_flour_summary(db: Session, centra_id: int = 0):
    today = date.today()
    query = db.query(models.Flour)
    
    if centra_id:
        query = query.filter(models.Flour.centra_id == centra_id)

    total = sum(flour.weight for flour in query.all())
    if total is None: total = 0
    monthly = sum(flour.weight for flour in get_flour_by_floured_date(db=db, centra_id=centra_id, year=today.year, month=today.month))/today.day
    if monthly is None: monthly = 0
    today = sum(flour.weight for flour in get_flour_by_floured_date(db=db, centra_id=centra_id, year=today.year, month=today.month, day=today.day))
    if today is None: today = 0
    
    return {"total": total, "monthly": monthly, "today": today}

def wash_wet_leaves(db: Session, id: int, date: schemas.DatetimeRecord):
    query = db.query(models.Wet).filter(models.Wet.id == id).update({models.Wet.washed_datetime: date.datetime})
    db.commit()
    return query

def dry_wet_leaves(db: Session, id: int, date: schemas.DatetimeRecord):
    query = db.query(models.Wet).filter(models.Wet.id == id).update({models.Wet.dried_datetime: date.datetime})
    db.commit()
    return query

def flour_dry_leaves(db: Session, id: int, date: schemas.DatetimeRecord):
    query = db.query(models.Dry).filter(models.Dry.id == id).update({models.Dry.floured_datetime: date.datetime})
    db.commit()
    return query

def get_packages_by_status(db: Session, status: int, centra_id: int = 0, skip:int = 0, limit:int = 30):
    query = db.query(models.PackageData).filter(models.PackageData.status == status)
    if centra_id: query = filter_by_centra_id(query, models.PackageData, centra_id)
    return query.offset(skip).limit(limit).all()

# def get_packages(db: Session):
#     query = db.query(models.PackageData).all()
#     return query

def get_packages(db: Session, centra_id: int=0):
    query = db.query(models.PackageData)
    if centra_id: query = filter_by_centra_id(query, models.PackageData, centra_id)
    return query.all()

def get_package_summary(db: Session, centra_id: int=0):
    query = db.query(models.PackageData)
    if centra_id: query = filter_by_centra_id(query, models.PackageData, centra_id)
    total = len(query.all())
    pending = len(query.filter(models.PackageData.status == 1).all())
    arrived  = len(query.filter(models.PackageData.status == 2 or models.PackageData.status == 3).all())
    return {"total": total, "pending": pending, "arrived": arrived}

def get_packages_created(db: Session, centra_id: int, year: int = 0, month: int = 0, day: int = 0, filter: str = "", skip: int = 0, limit: int = 20):
    query = db.query(models.PackageData).filter(models.PackageData.centra_id == centra_id)

    if year and month and day:
        if filter == "w":
            # Calculate start of week
            start_date = date(year, month, day) - timedelta(days=date(year, month, day).weekday())
            # Ensure the end date is the start date + 6 days to cover the whole week
            end_date = start_date + timedelta(days=6)
            query = query.filter(func.DATE(models.PackageData.created_datetime).between(start_date, end_date))
        else: query = query.filter(func.DATE(models.PackageData.created_datetime) == date(year, month, day))

    elif year:
        query = query.filter(extract("year", models.PackageData.created_datetime) == year)

        if month:
            query = query.filter(extract("month", models.PackageData.created_datetime) == month)

    if skip:
        query = query.offset(skip)
    
    if limit:
        query = query.limit(limit)  

    return query.all()
     

def get_shipping(db: Session, centra_id: int=0, year: int = 0, month: int = 0, day: int = 0, filter: str = "", skip: int = 0, limit: int = 20):
    query = db.query(models.Shipping)
    if centra_id: query = query.filter(models.Shipping.centra_id == centra_id)

    if year and month and day:
        if filter == "w":
            # Calculate start of week
            start_date = date(year, month, day) - timedelta(days=date(year, month, day).weekday())
            # Ensure the end date is the start date + 6 days to cover the whole week
            end_date = start_date + timedelta(days=6)
            query = query.filter(func.DATE(models.Shipping.departure_datetime).between(start_date, end_date))
        else: query = query.filter(func.DATE(models.Shipping.departure_datetime) == date(year, month, day))

    elif year:
        query = query.filter(extract("year", models.Shipping.departure_datetime) == year)

        if month:
            query = query.filter(extract("month", models.Shipping.departure_datetime) == month)

    if skip:
        query = query.offset(skip)
    
    if limit:
        query = query.limit(limit)  

    return query.all()

def get_shipment_summary(db: Session, centra_id: int = 0):
    today = date.today()
    query = db.query(models.Shipping)
    
    if centra_id:
        query = query.filter(models.Shipping.centra_id == centra_id)

    total = len(query.all())
    monthly = len(get_checkpoints(db=db, year=today.year, month=today.month))/today.day
    today = len(get_checkpoints(db=db, year=today.year, month=today.month, day=today.day))
    
    return {"total": total, "monthly": monthly, "today": today}

def get_centra_notifications(db: Session, centra_id: int = 0, skip: int = 0, limit: int = 100, date_filter: date = None, filter: Union[str, None] = None):
    query = db.query(models.CentraNotification)

    if filter == "before":
        query = query.filter(models.CentraNotification.date < date_filter)
    elif filter == "after":
            query = query.filter(models.CentraNotification.date > date_filter)
    elif filter == "during":
            query = query.filter(models.CentraNotification.date == date_filter)
    
    if centra_id: query = filter_by_centra_id(query, models.CentraNotification, centra_id)
    return query.offset(skip).limit(limit).all()

def get_guard_harbor_notifications(db: Session, skip: int = 0, limit: int = 100, date_filter: date = None, filter: Union[str, None] = None):
    query = db.query(models.GuardHarborNotification)

    if filter == "before":
        query = query.filter(models.GuardHarborNotification.date < date_filter)
    elif filter == "after":
            query = query.filter(models.GuardHarborNotification.date > date_filter)
    elif filter == "during":
            query = query.filter(models.GuardHarborNotification.date == date_filter)
    
    return query.offset(skip).limit(limit).all()

def get_reception_packages(db: Session, skip: int = 0, limit: int = 100, date_filter: datetime = None, before: bool = None, after: bool = None):
    query = db.query(models.ReceptionPackage)
    if date_filter:
        if before:
            query = query.filter(models.ReceptionPackage.receival_datetime < date_filter)
        elif after:
            query = query.filter(models.ReceptionPackage.receival_datetime > date_filter)
        else:
            query = query.filter(models.ReceptionPackage.receival_datetime == date_filter)
    return query.offset(skip).limit(limit).all()

def update_package_shipping_detail(db:Session, id:int, shipping_id:int):
    db_package = db.query(models.PackageData).filter(models.PackageData.id == id).first()
    setattr(db_package, "shipping_id", shipping_id,)
    update_package_status_by_id(db, id, 1)
    db.commit()
    db.refresh(db_package)
    return db_package

def update_rescaled(db:Session, id:int, rescaled_weight: float):
    db_rescaled = db.query(models.PackageData).filter(models.PackageData.id == id).first()
    setattr(db_rescaled, "weight", rescaled_weight)
    db.commit()
    db.refresh(db_rescaled)
    return db_rescaled

def update_reception_detail(db:Session, id:int, reception_id:int):
    db_package = db.query(models.PackageData).filter(models.PackageData.id == id).first()
    setattr(db_package, "reception_id", reception_id)
    setattr(db_package, "status", 3)
    db.commit()
    db.refresh(db_package)
    return db_package

def create_centra(db: Session, centra: schemas.CentraRecord):
    db_centra = models.Centra(location=centra.location)
    db.add(db_centra)
    db.commit()
    db.refresh(db_centra)
    return db_centra

def create_collection(db: Session, collection: schemas.CollectionRecord, user: models.Users):
    db_collection = models.Collection(retrieval_datetime=collection.retrieval_datetime, weight=collection.weight, centra_id=user.centra_unit)
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection


def create_wet_leaves(db: Session, wet_leaves: schemas.WetLeavesRecord, user: models.Users):
    db_wet_leaves = models.Wet(retrieval_date=wet_leaves.retrieval_date, weight=wet_leaves.weight, centra_id=user.centra_unit)
    db.add(db_wet_leaves)
    db.commit()
    db.refresh(db_wet_leaves)
    return db_wet_leaves

def create_dry_leaves(db: Session, dry_leaves: schemas.DryLeavesRecord, user: models.Users):
    db_dry_leaves = models.Dry(dried_date=dry_leaves.dried_date, weight=dry_leaves.weight, centra_id=user.centra_unit)
    db.add(db_dry_leaves)
    db.commit()
    db.refresh(db_dry_leaves)
    return db_dry_leaves

def create_flour(db: Session, flour: schemas.FlourRecord, user: models.Users):
    db_flour = models.Flour(**flour.model_dump(), centra_id=user.centra_unit)
    db.add(db_flour)
    db.commit()
    db.refresh(db_flour)
    return db_flour

def create_shipping(db: Session, shipping: schemas.ShippingInfoRecord, id):
    db_shipping = models.Shipping(**shipping.model_dump(exclude={"packages"}), centra_id=id)
    db.add(db_shipping)
    db.commit()
    db.refresh(db_shipping)
    return db_shipping

def create_checkpoint(db: Session, checkpoint: schemas.CheckpointDataRecord):
    db_checkpoint = models.CheckpointData(**checkpoint.model_dump(exclude="package_ids"))
    db.add(db_checkpoint)
    db.commit()
    db.refresh(db_checkpoint)
    return db_checkpoint

def create_package(db: Session, package: schemas.PackageCreate, id):
    db_package = models.PackageData(**package.model_dump(), centra_id=id, created_datetime=datetime.datetime.now())
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package

def create_centra_notifications(db: Session, message:str, id:int):
    db_centra_notif = models.CentraNotification(message=message, date=datetime.datetime.now(), centra_id=id)
    db.add(db_centra_notif)
    db.commit()
    db.refresh(db_centra_notif)
    return db_centra_notif

def create_GuardHarbor_notifications(db: Session, message:str, id:int, shipping_id:int):
    db_guard_harbor_notif = models.GuardHarborNotification(message=message, date=datetime.datetime.now(), centra_id=id, shipping_id=shipping_id)
    db.add(db_guard_harbor_notif)
    db.commit()
    db.refresh(db_guard_harbor_notif)
    return db_guard_harbor_notif

def create_reception_packages(db: Session, reception_packages: schemas.ReceptionPackageRecord):
    db_reception_packages = models.ReceptionPackage(**reception_packages.model_dump(exclude={"package_id"}), package_id=str(reception_packages.package_id).strip("[]"))
    db.add(db_reception_packages)
    db.commit()
    db.refresh(db_reception_packages)
    return db_reception_packages

def create_rescaled_package_data(db: Session, package_id: int, rescaled_weight: float, materials_to_cover: str):
    db_rescaled_package_data = models.RescaledPackageData(package_id=package_id, rescaled_weight=rescaled_weight, materials_to_cover=materials_to_cover)
    db.add(db_rescaled_package_data)
    db.commit()
    db.refresh(db_rescaled_package_data)
    return db_rescaled_package_data

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

def update_shipping_arrival(db: Session, shipping_id: int, arrival_datetime: datetime):
    shipping = db.query(models.Shipping).filter(models.Shipping.id == shipping_id).first()
    if shipping:
        shipping.arrival_datetime = arrival_datetime
        db.commit()
        db.refresh(shipping)
    return shipping


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

def update_package_status_by_id(db: Session, package_id: int, status: int):
    db_package = get_package_by_id(db, package_id)
    if db_package:
        setattr(db_package, "status", status)
        db.commit()
        db.refresh(db_package)

        return db_package
    return None

def update_package_status(db: Session, db_package: models.PackageData, status: int):
    if db_package:
        setattr(db_package, "status", status)
        db.commit()
        db.refresh(db_package)

        return db_package
    return None

def update_package_receival_datetime(db: Session, package_id: int, received_datetime: datetime):
    db_package = get_package_by_id(db, package_id)
    if db_package:
        setattr(db_package, "received_datetime", received_datetime)
        db.commit()
        db.refresh(db_package)
        print(received_datetime)

        return db_package 
    return None

def check_package_expiry(db: Session):
    now = date.utcnow()
    expired_packages = db.query(models.PackageData).filter(models.PackageData.status < 4, models.PackageData.exp_date < now).all()
    for package in expired_packages:
        package.status = 4  
        db.commit()
        db.refresh(package)
    return expired_packages

def delete_centra(db: Session, centra_id: int):
    db_centra = get_centra_by_id(db, centra_id)
    if db_centra:
        db.delete(db_centra)
        db.commit()
    return db_centra

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

def delete_package(db: Session, package_id: int):
    db_package = get_package_by_id(db, package_id)
    if db_package:
        db.delete(db_package)
        db.commit()
    return db_package
