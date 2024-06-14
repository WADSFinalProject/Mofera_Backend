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
    prefix="/guard_harbor",
    tags=["guard_harbor"]
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

@router.post("/add_checkpoint", dependencies=[Depends(role_access(RoleEnum.GuardHarbor))])
def add_checkpoint_data(checkpoint: schemas.CheckpointDataRecord, db: db_dependecy):
    db_checkpoint = crud.create_checkpoint(db=db, checkpoint=checkpoint)
    for id in checkpoint.package_ids:
        print(id)
        crud.update_checkpoint(db=db, id=id,)
    return JSONResponse(content={"detail": "checkpoint record added successfully"}, status_code=status.HTTP_201_CREATED)

# @router.post("/update_checkpoint", dependencies=[Depends(role_access(RoleEnum.GuardHarbor))])
# def update_checkpoint_data(checkpoint_id: int, checkpoint: schemas.CheckpointDataRecord, db: db_dependecy):
#     db_checkpoint = crud.update_checkpoint(db=db, checkpoint_id=checkpoint_id, checkpoint=checkpoint,  )
#     return JSONResponse(content={"detail": "Checkpoint data updated successfully"}, status_code=status.HTTP_200_OK)

# @router.put("/confirm/arrival/{id}", dependencies=[Depends(role_access(RoleEnum.GuardHarbor))])
# def confirm_arrival(id: int, db: db_dependecy):
#     db_checkpoint = crud.update_package_status(db=db, id=id, status=2)
#     return JSONResponse(content={"detail": "Arrival confirmed successfully"}, status_code=status.HTTP_200_OK)

#delete checkpoint endpoint
@router.post("/delete_checkpoint", dependencies=[Depends(role_access(RoleEnum.GuardHarbor))])
def delete_checkpoint_data(checkpoint_id: int, db: db_dependecy):
    db_checkpoint = crud.delete_checkpoint(db=db, checkpoint_id=checkpoint_id)
    return JSONResponse(content={"detail": "Checkpoint data deleted successfully"}, status_code=status.HTTP_200_OK)

@router.get("/shipping", dependencies=[Depends(role_access(RoleEnum.GuardHarbor))])
def get_shipping(db: db_dependecy):
    db_shipping = crud.get_shipping(db=db)
    return db_shipping

@router.get("/packages", dependencies=[Depends(role_access(RoleEnum.GuardHarbor))])
def get_packages(db: db_dependecy):
    db_packages = crud.get_packages(db=db)
    return db_packages
