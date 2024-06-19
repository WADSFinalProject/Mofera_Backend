from fastapi.responses import JSONResponse
from jose import jwt
import requests
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users, RefreshToken
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta, date
from jose import jwt, JWTError
from typing import Optional
import logging
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel
import schemas
import crud
import calendar

from auth import role_access, get_db, get_current_user
from models import Users
from roles_enum import RoleEnum

router = APIRouter(
    prefix="/centra",
    tags=["centra"]
)
SECRET_KEY = '194679e3j938492938382883dej3ioms998323ftu933@jd7233!'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
# auth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependecy = Annotated[Session, Depends(get_db)]

logger = logging.getLogger(__name__)

@router.post("/new_wet_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_wet_leaves(wet_leaves: schemas.WetLeavesRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_wet = crud.create_wet_leaves(db=db, wet_leaves=wet_leaves, user=current_user)
    crud.create_centra_notifications(db=db, message=f"New wet leaves added - Wet#{db_wet.id}", id=current_user.centra_unit)
    return JSONResponse(content={"detail": "Wet leaves record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.post("/new_collection", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_collection(collection: schemas.CollectionRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_collection = crud.create_collection(db=db, collection=collection, user=current_user)
    crud.create_centra_notifications(db=db, message=f"New collection added - Collection#{db_collection.id}", id=current_user.centra_unit)
    return JSONResponse(content={"detail": "Collection record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.post("/new_dry_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_dry_leaves(dry_leaves: schemas.DryLeavesRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_dry = crud.create_dry_leaves(db=db, dry_leaves=dry_leaves, user=current_user)
    crud.create_centra_notifications(db=db, message=f"New dry added - Dry#{db_dry.id}", id=current_user.centra_unit)
    return JSONResponse(content={"detail": "Dry leaves record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.post("/new_flour", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_flour(flour: schemas.FlourRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_flour = crud.create_flour(db=db, flour=flour, user=current_user)
    crud.create_centra_notifications(db=db, message=f"New flour added - Flour#{db_flour.id}", id=current_user.centra_unit)
    return JSONResponse(content={"detail": "Flour record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.get("/location", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_centra_location(db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_centra = crud.get_centra_by_id(db=db, centra_id=int(current_user.centra_unit))
    if not db_centra:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Centra not found")
    return db_centra

@router.get("/collection", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_collection(db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_collection = crud.get_collection(db=db, centra_id=int(current_user.centra_unit))
    return db_collection

@router.get("/wet_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_wet_leaves(db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_wet_leaves = crud.get_wet_leaves(db=db, centra_id=int(current_user.centra_unit))
    return db_wet_leaves

@router.get("/washed_wet_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_washed_wet_leaves(db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_washed_wet_leaves = crud.get_washed_wet_leaves(db=db, centra_id=int(current_user.centra_unit))
    return db_washed_wet_leaves

@router.get("/dry_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_dry_leaves(db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_dry_leaves = crud.get_dry_leaves(db=db, centra_id=int(current_user.centra_unit))
    return db_dry_leaves

@router.get("/dry_leaves_mobile", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_dry_leaves_mobile(date: date, interval: str, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_dry_leaves = crud.get_dry_leaves_mobile(db=db, date_origin=date, interval=interval, centra_id=int(current_user.centra_unit))
    return db_dry_leaves

@router.get("/flour", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_flour(db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_flour = crud.get_flour(db=db, centra_id=int(current_user.centra_unit))
    return db_flour

# @router.get("/packages", dependencies=[Depends(role_access(RoleEnum.centra))])
# def get_packages(db: db_dependecy):
#     db_packages = crud.get_packages(db=db)
#     return db_packages

@router.get("/packages", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_packages(db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_packages = crud.get_packages(db=db, centra_id=int(current_user.centra_unit))
    for package in db_packages:
        if package.exp_date <= date.today() and package.status != 3:
            crud.update_package_status(db=db, db_package=package, status=4)
    db_packages = crud.get_packages(db=db, centra_id=int(current_user.centra_unit))
    return db_packages

@router.get("/packages_status", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_packages_with_status(status: int, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_packages = crud.get_packages_by_status(db=db, status=status, centra_id=int(current_user.centra_unit) )
    return db_packages

@router.get("/notification", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_notification(db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_packages = crud.get_centra_notifications(db=db, centra_id=int(current_user.centra_unit))
    return db_packages

@router.get("/recent_notification", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_recent_notification(db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_packages = crud.get_recent_centra_notifications(db=db, centra_id=int(current_user.centra_unit))
    return db_packages

@router.get("/shippings", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_shipping(db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_shipping = crud.get_shipping(db=db, centra_id=int(current_user.centra_unit))
    return db_shipping

@router.get("/checkpoints", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_checkpoint(db: db_dependecy):
    db_checkpoint = crud.get_checkpoints(db=db)
    return db_checkpoint

@router.put("/wash_wet_leaves/{id}", dependencies=[Depends(role_access(RoleEnum.centra))])
def wash_wet_leaves(id:int, date:schemas.DatetimeRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    query = crud.wash_wet_leaves(db=db, id=id, date=date)
    crud.create_centra_notifications(db=db, message=f"Washing Wet#{id}", id=current_user.centra_unit)
    return 

@router.put("/dry_wet_leaves/{id}", dependencies=[Depends(role_access(RoleEnum.centra))])
def dry_wet_leaves(id:int, date:schemas.DatetimeRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    query = crud.dry_wet_leaves(db=db, id=id, date=date)
    crud.create_centra_notifications(db=db, message=f"Drying Wet#{id}", id=current_user.centra_unit)
    return

@router.put("/flour_dry_leaves/{id}", dependencies=[Depends(role_access(RoleEnum.centra))])
def flour_dry_leaves(id:int, date:schemas.DatetimeRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    query = crud.flour_dry_leaves(db=db, id=id, date=date)
    crud.create_centra_notifications(db=db, message=f"Flouring Dry#{id}", id=current_user.centra_unit)
    return 

@router.post("/add_package", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_package(record:schemas.PackageCreate, db:db_dependecy, current_user: Users = Depends(get_current_user)):
    query = crud.create_package(db=db, package=record, id=current_user.centra_unit)
    crud.create_centra_notifications(db=db, message=f"New package added - Package#{query.id}", id=current_user.centra_unit)

@router.post("/add_shipping", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_shipping_info(shipping:schemas.ShippingInfoRecord, db:db_dependecy, current_user: Users = Depends(get_current_user)):
    db_shipping = crud.create_shipping(db=db, shipping=shipping, id=current_user.centra_unit)
    for id in shipping.packages:
        crud.update_package_shipping_detail(db=db, id=id, shipping_id=db_shipping.id )
    crud.create_centra_notifications(db=db, message=f"New shipping added - Shipping#{db_shipping.id}", id=current_user.centra_unit)
    crud.create_GuardHarbor_notifications(db=db, message=f'<b style="color: primary;">Shipping ID #{db_shipping.id}</b> has been shipped by Centra {db_shipping.centra_id}', id=current_user.centra_unit, shipping_id=db_shipping.id)

@router.get("/reception_packages", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_reception_packages(db: db_dependecy):
    db_reception = crud.get_reception_packages(db=db)
    return db_reception

@router.get("/quick_get_wet_stats", dependencies=[Depends(role_access(RoleEnum.centra))])
def quick_get_wet_statistics(db:db_dependecy, interval:str, date:date = date.today(), slice:int = 5, current_user: Users = Depends(get_current_user)):
    label = list()
    data = list()
    if interval == "daily":
        for offset in range(slice):
            offset_date = date - timedelta(days=offset)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(sum(wet.weight for wet in crud.get_wet_leaves(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day)))
    
    elif interval == "weekly":
        for offset in range(slice):
            offset_date = date - timedelta(days=date.weekday()+1+(offset-1)*7)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(sum(wet.weight for wet in crud.get_wet_leaves(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day, filter="w")))
    
    elif interval == "monthly":
        for offset in range(slice):
            offset_date = date.replace(year= date.year-1 if date.month-offset < 1  else date.year, month=date.month-offset if date.month-offset > 0 else 12)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]
).strftime("%Y-%m"))
            data.append(sum(wet.weight for wet in crud.get_wet_leaves(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year, month=offset_date.month)))
    
    elif interval == "annually":
        for offset in range(slice):
            offset_date = date.replace(year=date.year-offset)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]).strftime("%Y"))
            data.append(sum(wet.weight for wet in crud.get_wet_leaves(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year)))
    label.reverse()
    data.reverse()

    return {"label":label, "data":data}

@router.get("/quick_get_dry_stats", dependencies=[Depends(role_access(RoleEnum.centra))])
def quick_dry_quick_statistics(db:db_dependecy, interval:str, date:date = date.today(), current_user: Users = Depends(get_current_user), slice:int = 5):
    label = list()
    data = list()
    if interval == "daily":
        for offset in range(slice):
            offset_date = date - timedelta(days=offset)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(sum(dry.weight for dry in crud.get_dry_leaves_by_dried_date(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day)))
    
    elif interval == "weekly":
        for offset in range(slice):
            offset_date = date - timedelta(days=date.weekday()+1+(offset-1)*7)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(sum(dry.weight for dry in crud.get_dry_leaves_by_dried_date(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day, filter="w")))
    
    elif interval == "monthly":
        for offset in range(slice):
            offset_date = date.replace(year= date.year-1 if date.month-offset < 1  else date.year, month=date.month-offset if date.month-offset > 0 else 12)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]
).strftime("%Y-%m"))
            data.append(sum(dry.weight for dry in crud.get_dry_leaves_by_dried_date(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year, month=offset_date.month)))
    
    elif interval == "annually":
        for offset in range(slice):
            offset_date = date.replace(year=date.year-offset)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]).strftime("%Y"))
            data.append(sum(dry.weight for dry in crud.get_dry_leaves_by_dried_date(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year)))
    label.reverse()
    data.reverse()

    return {"label":label, "data":data}

@router.get("/quick_get_flour_stats", dependencies=[Depends(role_access(RoleEnum.centra))])
def quick_get_flour_statistics(db:db_dependecy, interval:str, date:date = date.today(), current_user: Users = Depends(get_current_user), slice:int = 5):
    label = list()
    data = list()
    if interval == "daily":
        for offset in range(slice):
            offset_date = date - timedelta(days=offset)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(sum(flour.weight for flour in crud.get_flour_by_floured_date(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day)))
    
    elif interval == "weekly":
        for offset in range(slice):
            offset_date = date - timedelta(days=date.weekday()+1+(offset-1)*7)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(sum(flour.weight for flour in crud.get_flour_by_floured_date(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day, filter="w")))
    
    elif interval == "monthly":
        for offset in range(slice):
            offset_date = date.replace(year= date.year-1 if date.month-offset < 1  else date.year, month=date.month-offset if date.month-offset > 0 else 12)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]
).strftime("%Y-%m"))
            data.append(sum(flour.weight for flour in crud.get_flour_by_floured_date(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year, month=offset_date.month)))
    
    elif interval == "annually":
        for offset in range(slice):
            offset_date = date.replace(year=date.year-offset)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]).strftime("%Y"))
            data.append(sum(flour.weight for flour in crud.get_flour_by_floured_date(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year)))
    label.reverse()
    data.reverse()

    return {"label":label, "data":data}

@router.get("/quick_get_package_stats", dependencies=[Depends(role_access(RoleEnum.centra))])
def quick_get_package_statistics(db:db_dependecy, interval: str, date: date = date.today(), current_user: Users = Depends(get_current_user), slice: int = 5):
    label = list()
    data = list()

    if interval == "daily":
        for offset in range(slice):
            offset_date = date - timedelta(days=offset)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(len(crud.get_packages_created(db=db, centra_id=int(current_user.centra_unit) ,year=offset_date.year, month=offset_date.month, day=offset_date.day)))
    
    elif interval == "weekly":
        for offset in range(slice):
            offset_date = date - timedelta(days=date.weekday()+1+(offset-1)*7)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(len(crud.get_packages_created(db=db, centra_id=int(current_user.centra_unit), limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day, filter="w")))
    
    elif interval == "monthly":
        for offset in range(slice):
            offset_date = date.replace(year=date.year - 1 if date.month - offset < 1 else date.year, month=date.month - offset if date.month - offset > 0 else 12)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]).strftime("%Y-%m"))
            data.append(len(crud.get_packages_created(db=db, centra_id=int(current_user.centra_unit), year=offset_date.year, month=offset_date.month)))
    
    elif interval == "annually":
        for offset in range(slice):
            offset_date = date.replace(year=date.year - offset)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]).strftime("%Y"))
            data.append(len(crud.get_packages_created(db=db, centra_id=int(current_user.centra_unit), year=offset_date.year)))

    label.reverse()
    data.reverse()

    return {"label":label, "data":data}