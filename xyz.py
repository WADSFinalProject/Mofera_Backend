from fastapi.responses import JSONResponse
from jose import jwt
import requests
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users, RefreshToken
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
import logging
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel
import models
import schemas
import crud

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

@router.get("/get_package", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_package(db:db_dependecy, s:str = "", p: int = 0):

    db_package = crud.get_packages_by_status(db=db, status=2, skip=p*30, limit=(p+1)*30)
    return db_package

@router.get("/get_wet_stats", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_wet_statistics(db:db_dependecy, p: int = 0, year:int=0, month:int=0, day:int=0, filter:str=""):

    db_wet = crud.get_wet_leaves(db=db, limit=0, year=year, month=month, day=day, filter=filter)
    total_weight = sum(wet.weight for wet in db_wet)
    return {"total_weight": total_weight}

@router.get("/get_dry_stats", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_dry_statistics(db:db_dependecy, p: int = 0, year:int=0, month:int=0, day:int=0, filter:str=""):

    db_dry = crud.get_dry_leaves_by_dried_date(db=db, limit=0, year=year, month=month, day=day, filter=filter)
    total_weight = sum(flour.weight for flour in db_dry)
    return {"total_weight": total_weight}

@router.get("/get_flour_stats", dependencies=[Depends(role_access(RoleEnum.xyz))])
def get_flour_statistics(db:db_dependecy, p: int = 0, year:int=0, month:int=0, day:int=0, filter:str=""):

    db_flour = crud.get_flour_by_floured_date(db=db, limit=0, year=year, month=month, day=day, filter=filter)
    total_weight = sum(flour.weight for flour in db_flour)
    return {"total_weight": total_weight}

@router.put("/rescale/{id}", dependencies=[Depends(role_access(RoleEnum.xyz))])
def rescale_package(id: int, rescale: schemas.RescaledRecord, db:db_dependecy):
    db_rescaled_package = crud.update_rescaled(db=db, id=id, rescaled_weight=rescale.weight)
    db_rescale_record = crud.create_rescaled_package_data(db=db, package_id=id, rescaled_weight=rescale.weight, materials_to_cover=rescale.material)
    return JSONResponse(content={"detail": "rescale record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.put("/collect/package/{id}", dependencies=[Depends(role_access(RoleEnum.xyz))])
def collect_package(id: int, db: db_dependecy):
    db_collect = crud.update_package_status(db=db, id=id, status=3)
    return JSONResponse(content={"detail": "receival record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.post("/add_reception", dependencies=[Depends(role_access(RoleEnum.xyz))])
def add_checkpoint_data(reception: schemas.ReceptionPackageRecord, db: db_dependecy):
    db_reception = crud.create_reception_packages(db=db, reception_packages=reception)
    for id in reception.package_id:
        crud.update_reception_detail(db=db, id=id, reception_id=db_reception.id)
    return JSONResponse(content={"detail": "reception record added successfully"}, status_code=status.HTTP_201_CREATED)
