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
import schemas
import crud

from auth import role_access, get_db
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

@router.post("/new_collection", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_collection(collection: schemas.CollectionRecord, db: db_dependecy):
    db_collection = crud.create_collection()
    return JSONResponse(content={"detail": "Collection record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.post("/new_wet_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_wet_leaves(wet_leaves: schemas.WetLeavesRecord, db: db_dependecy):
    db_collection = crud.create_wet_leaves(db=db, wet_leaves=wet_leaves)
    return JSONResponse(content={"detail": "Wet leaves record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.post("/new_dry_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_dry_leaves(dry_leaves: schemas.DryLeavesRecord, db: db_dependecy):
    db_dry = crud.create_dry_leaves(db=db, dry_leaves=dry_leaves)
    return JSONResponse(content={"detail": "Dry leaves record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.post("/new_flour", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_flour(flour: schemas.FlourRecord, db: db_dependecy):
    db_flour = crud.create_flour(db=db, flour=flour)
    return JSONResponse(content={"detail": "Flour record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.get("/collection", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_collection(db: db_dependecy):
    db_collection = crud.get_collection(db=db)
    return db_collection

@router.get("/wet_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_wet_leaves(db: db_dependecy):
    db_wet_leaves = crud.get_wet_leaves(db=db)
    return db_wet_leaves

@router.get("/dry_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_dry_leaves(db: db_dependecy):
    db_dry_leaves = crud.get_dry_leaves(db=db)
    return db_dry_leaves

@router.get("/flour", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_flour(db: db_dependecy):
    db_flour = crud.get_flour(db=db)
    return db_flour

@router.get("/packages", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_packages(db: db_dependecy):
    db_packages = crud.get_packages(db=db)
    return db_packages

@router.put("/wash_wet_leaves/{id}", dependencies=[Depends(role_access(RoleEnum.centra))])
def wash_wet_leaves(id:int, date:schemas.DateRecord, db: db_dependecy):
    query = crud.wash_wet_leaves(db=db, id=id, date=date)
    return 

@router.put("/dry_wet_leaves/{id}", dependencies=[Depends(role_access(RoleEnum.centra))])
def dry_wet_leaves(id:int, date:schemas.DateRecord, db: db_dependecy):
    query = crud.dry_wet_leaves(db=db, id=id, date=date)
    return

@router.put("/flour_dry_leaves/{id}", dependencies=[Depends(role_access(RoleEnum.centra))])
def flour_dry_leaves(id:int, date:schemas.DateRecord, db: db_dependecy):
    query = crud.flour_dry_leaves(db=db, id=id, date=date)
    return 

@router.post("/add_package", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_package(record:schemas.packageRecord, db:db_dependecy):
    query = crud.create_package(db=db, package=record)

@router.post("/add_shipping", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_shipping_info(shipping:schemas.ShippingInfoRecord, db:db_dependecy):
    db_shipping = crud.create_shipping(db=db, shipping=shipping)
    for id in shipping.packages:
        crud.update_package_shipping_detail(db=db, id=id, shipping_id=db_shipping.id)
    