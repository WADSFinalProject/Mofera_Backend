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
import models
import schemas
import crud
import calendar

from auth import role_access, get_db
from roles_enum import RoleEnum

router = APIRouter(
    prefix="/xyz",
    tags=["xyz"]
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

@router.get("/get_package_by_id", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_package(db:db_dependecy, s:str = ""):

    db_package = crud.get_package_by_id(db=db, package_id=s)
    return db_package

@router.get("/get_package", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_package(db:db_dependecy, s:str = "", p: int = 0):

    db_package = crud.get_packages_by_status(db=db, status=2, skip=p*30, limit=(p+1)*30)
    return db_package

@router.get("/quick_get_wet_stats", dependencies=[Depends(role_access(RoleEnum.xyz))])
def quick_get_wet_statistics(db:db_dependecy, interval:str, date:date = date.today(), slice:int = 6):
    label = list()
    data = list()
    if interval == "daily":
        for offset in range(slice):
            offset_date = date - timedelta(days=offset)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(sum(wet.weight for wet in crud.get_wet_leaves(db=db, limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day)))
    
    elif interval == "weekly":
        for offset in range(slice):
            offset_date = date - timedelta(days=date.weekday()+1+(offset-1)*7)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(sum(wet.weight for wet in crud.get_wet_leaves(db=db, limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day, filter="w")))
    
    elif interval == "monthly":
        for offset in range(slice):
            offset_date = date.replace(year= date.year-1 if date.month-offset < 1  else date.year, month=date.month-offset if date.month-offset > 0 else 12)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]
).strftime("%Y-%m"))
            data.append(sum(wet.weight for wet in crud.get_wet_leaves(db=db, limit=0, year=offset_date.year, month=offset_date.month)))
    
    elif interval == "yearly":
        for offset in range(slice):
            offset_date = date.replace(year=date.year-offset)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]).strftime("%Y"))
            data.append(sum(wet.weight for wet in crud.get_wet_leaves(db=db, limit=0, year=offset_date.year)))
    label.reverse()
    data.reverse()

    return {"label":label, "data":data}

@router.get("/get_wet_datas", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_wet_datas(db:db_dependecy, p: int = 0):

    db_wet = crud.get_wet_leaves(db=db, limit=50,)
    return db_wet

@router.get("/quick_get_dry_stats", dependencies=[Depends(role_access(RoleEnum.xyz))])
def quick_dry_quick_statistics(db:db_dependecy, interval:str, date:date = date.today(), slice:int = 6):
    label = list()
    data = list()
    if interval == "daily":
        for offset in range(slice):
            offset_date = date - timedelta(days=offset)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(sum(dry.weight for dry in crud.get_dry_leaves_by_dried_date(db=db, limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day)))
    
    elif interval == "weekly":
        for offset in range(slice):
            offset_date = date - timedelta(days=date.weekday()+1+(offset-1)*7)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(sum(dry.weight for dry in crud.get_dry_leaves_by_dried_date(db=db, limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day, filter="w")))
    
    elif interval == "monthly":
        for offset in range(slice):
            offset_date = date.replace(year= date.year-1 if date.month-offset < 1  else date.year, month=date.month-offset if date.month-offset > 0 else 12)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]
).strftime("%Y-%m"))
            data.append(sum(dry.weight for dry in crud.get_dry_leaves_by_dried_date(db=db, limit=0, year=offset_date.year, month=offset_date.month)))
    
    elif interval == "yearly":
        for offset in range(slice):
            offset_date = date.replace(year=date.year-offset)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]).strftime("%Y"))
            data.append(sum(dry.weight for dry in crud.get_dry_leaves_by_dried_date(db=db, limit=0, year=offset_date.year)))
    label.reverse()
    data.reverse()

    return {"label":label, "data":data}

@router.get("/get_dry_datas", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_dry_datas(db:db_dependecy, p: int = 0):

    db_dry = crud.get_dry_leaves(db=db, limit=50,)
    return db_dry

@router.get("/quick_get_flour_stats", dependencies=[Depends(role_access(RoleEnum.xyz))])
def quick_get_flour_statistics(db:db_dependecy, interval:str, date:date = date.today(), slice:int = 6):
    label = list()
    data = list()
    if interval == "daily":
        for offset in range(slice):
            offset_date = date - timedelta(days=offset)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(sum(flour.weight for flour in crud.get_flour_by_floured_date(db=db, limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day)))
    
    elif interval == "weekly":
        for offset in range(slice):
            offset_date = date - timedelta(days=date.weekday()+1+(offset-1)*7)
            label.append(offset_date.strftime("%d/%m/%Y"))
            data.append(sum(flour.weight for flour in crud.get_flour_by_floured_date(db=db, limit=0, year=offset_date.year, month=offset_date.month, day=offset_date.day, filter="w")))
    
    elif interval == "monthly":
        for offset in range(slice):
            offset_date = date.replace(year= date.year-1 if date.month-offset < 1  else date.year, month=date.month-offset if date.month-offset > 0 else 12)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]
).strftime("%Y-%m"))
            data.append(sum(flour.weight for flour in crud.get_flour_by_floured_date(db=db, limit=0, year=offset_date.year, month=offset_date.month)))
    
    elif interval == "yearly":
        for offset in range(slice):
            offset_date = date.replace(year=date.year-offset)
            label.append(offset_date.replace(day=calendar.monthrange(offset_date.year, offset_date.month)[1]).strftime("%Y"))
            data.append(sum(flour.weight for flour in crud.get_flour_by_floured_date(db=db, limit=0, year=offset_date.year)))
    label.reverse()
    data.reverse()

    return {"label":label, "data":data}

@router.get("/get_flour_stats", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_flour_statistics(db:db_dependecy, p: int = 0, year:int=0, month:int=0, day:int=0, filter:str=""):

    db_flour = crud.get_flour_by_floured_date(db=db, limit=0, year=year, month=month, day=day, filter=filter)
    total_weight = sum(flour.weight for flour in db_flour)
    return {"total_weight": total_weight}

@router.get("/get_flour_datas", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_flour_datas(db:db_dependecy, p: int = 0):

    db_flour = crud.get_flour(db=db, limit=50,)
    return db_flour

@router.get("/get_reception", dependencies=[Depends(role_access(RoleEnum.xyz))])
def add_checkpoint_data(db: db_dependecy):
    db_reception = crud.get_reception_packages(db=db)
    return db_reception

@router.get("/search_reception", dependencies=[Depends(role_access(RoleEnum.xyz))])
def search_reception(id:int, db: db_dependecy):
    db_reception = crud.get_reception_packages_by_id(db=db, reception_packages_id=id)
    return db_reception

@router.get("/search_package_rescale", dependencies=[Depends(role_access(RoleEnum.xyz))])
def search_package_rescale(db:db_dependecy, s: str = ""):
    db_package = crud.get_package_by_id(db=db, package_id=s)
    print(db_package)
    if db_package is None or db_package.status != 2:
        return None
    
    return db_package

@router.get("/get_shipment_notification", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_shipping_notification(db:db_dependecy, p: int = 0):

    db_shipping = crud.get_shipping(db=db, limit=50,)
    return [{
        "id":shipping.id,
        "shipper":f"Centra {shipping.centra_id}",
        "timestamp": shipping.departure_datetime,
        "estimatedArrival": shipping.eta_datetime,
    } for shipping in db_shipping]

@router.get("/get_arrival_notification", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_arrival_notification(db:db_dependecy, p: int = 0):

    db_checkpoint = crud.get_checkpoints(db=db, limit=50,)
    return [{
        "id":checkpoint.id,
        "shipper":f"Centra {crud.get_shipping_by_id(db=db, shipping_id=checkpoint.shipping_id).centra_id}",
        "timestamp": checkpoint.arrival_datetime,
    } for checkpoint in db_checkpoint]

@router.put("/rescale/{id}", dependencies=[Depends(role_access(RoleEnum.xyz))])
def rescale_package(id: int, rescale: schemas.RescaledRecord, db:db_dependecy):
    db_rescaled_package = crud.update_rescaled(db=db, id=id, rescaled_weight=rescale.weight)
    db_rescale_record = crud.create_rescaled_package_data(db=db, package_id=id, rescaled_weight=rescale.weight, materials_to_cover=rescale.material)
    return JSONResponse(content={"detail": "rescale record added successfully"}, status_code=status.HTTP_201_CREATED)

# @router.put("/collect/package/{id}", dependencies=[Depends(role_access(RoleEnum.xyz))])
# def collect_package(id: int, db: db_dependecy):
#     db_collect = crud.update_package_status(db=db, id=id, status=3)
#     return JSONResponse(content={"detail": "receival record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.post("/add_reception", dependencies=[Depends(role_access(RoleEnum.xyz))])
def add_reception_data(reception: schemas.ReceptionPackageRecord, db: db_dependecy):
    db_reception = crud.create_reception_packages(db=db, reception_packages=reception)
    for id in reception.package_id:
        crud.update_reception_detail(db=db, id=id, reception_id=db_reception.id)
    return JSONResponse(content={"detail": "reception record added successfully", "id": db_reception.id}, status_code=status.HTTP_201_CREATED)

@router.get("/checkpoints", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_checkpoint(db: db_dependecy):
    db_checkpoint = crud.get_checkpoints(db=db)
    return db_checkpoint

@router.get("/packages_status", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_packages_with_status(status: int, db: db_dependecy):
    db_packages = crud.get_packages_by_status(db=db, status=status)
    return db_packages

@router.get("/reception_packages", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_reception_packages(db: db_dependecy):
    db_reception = crud.get_reception_packages(db=db)
    return db_reception

@router.get("/packages", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_packages(db: db_dependecy):
    db_packages = crud.get_packages(db=db)
    return db_packages

@router.get("/shipping", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_shipping(db: db_dependecy):
    db_shipping = crud.get_shipping(db=db)
    return db_shipping
