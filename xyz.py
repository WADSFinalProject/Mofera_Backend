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

@router.put("/rescale/{id}", dependencies=[Depends(role_access(RoleEnum.xyz))])
def rescale_package(id: int, rescale: schemas.RescaledRecord, db:db_dependecy):
    db_rescaled = crud.update_rescaled(db=db, id=id, rescaled_weight=rescale.weight)
    return JSONResponse(content={"detail": "checkpoint record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.put("/collect/package/{id}", dependencies=[Depends(role_access(RoleEnum.xyz))])
def collect_package(id: int, db: db_dependecy):
    db_collect = crud.update_package_status(db=db, id=id, status=3)
    return JSONResponse(content={"detail": "checkpoint record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.post("/add_reception", dependencies=[Depends(role_access(RoleEnum.xyz))])
def add_checkpoint_data(reception: schemas.ReceptionPackageRecord, db: db_dependecy):
    db_reception = crud.create_reception_packages(db=db, reception_packages=reception)
    for id in reception.package_id:
        crud.update_reception_detail(db=db, id=id, reception_id=db_reception.id)
    return JSONResponse(content={"detail": "checkpoint record added successfully"}, status_code=status.HTTP_201_CREATED)
