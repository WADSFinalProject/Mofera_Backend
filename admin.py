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
    prefix="/admin",
    tags=["admin"]
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

@router.get("/users", dependencies=[Depends(role_access(RoleEnum.admin))])
def get_user(db:db_dependecy, s:str = "", p: int = 0):

    db_user = crud.get_users(db=db)
    return db_user

@router.get("/centra", dependencies=[Depends(role_access(RoleEnum.admin))])
def get_centra(db:db_dependecy, s:str = "", p: int = 0):

    db_centra = crud.get_centra(db=db)
    return db_centra


@router.get("/wet_leaves", dependencies=[Depends(role_access(RoleEnum.admin))])
def get_wet_leaves(db: db_dependecy):
    db_wet_leaves = crud.get_wet_leaves(db=db)
    return db_wet_leaves

@router.get("/dry_leaves", dependencies=[Depends(role_access(RoleEnum.admin))])
def get_dry_leaves(db: db_dependecy):
    db_dry_leaves = crud.get_dry_leaves(db=db)
    return db_dry_leaves

@router.get("/flour", dependencies=[Depends(role_access(RoleEnum.admin))])
def get_flour(db: db_dependecy):
    db_flour = crud.get_flour(db=db)
    return db_flour

@router.get("/shipping", dependencies=[Depends(role_access(RoleEnum.admin))])
def get_shipping(db: db_dependecy):
    db_shipping = crud.get_shipping(db=db)
    return db_shipping

@router.get("/checkpoints", dependencies=[Depends(role_access(RoleEnum.admin))])
def get_checkpoint(db: db_dependecy):
    db_checkpoint = crud.get_checkpoints(db=db)
    return db_checkpoint

@router.get("/packages", dependencies=[Depends(role_access(RoleEnum.admin))])
def get_packages(db: db_dependecy):
    db_packages = crud.get_packages(db=db)
    return db_packages

