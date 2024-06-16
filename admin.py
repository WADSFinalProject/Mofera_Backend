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
import auth

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

@router.put("/users/{user_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
def update_user(user_id: int, user: schemas.UserUpdate, db: db_dependecy):
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = crud.update_user(db=db, user=db_user, user_update=user)
    return updated_user

# @router.put("/packages/{package_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
# def update_package(package_id: int, package: schemas.PackageUpdate, db: db_dependecy):
#     db_package = crud.get_package_by_id(db=db, package_id=package_id)
#     if not db_package:
#         raise HTTPException(status_code=404, detail="Package not found")
#     updated_package = crud.update_package(db=db, package=db_package, package_update=package)
#     return updated_package

# @router.put("/checkpoints/{checkpoint_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
# def update_checkpoint(checkpoint_id: int, checkpoint: schemas.CheckpointUpdate, db: db_dependecy):
#     db_checkpoint = crud.get_checkpoint_by_id(db=db, checkpoint_id=checkpoint_id)
#     if not db_checkpoint:
#         raise HTTPException(status_code=404, detail="Checkpoint not found")
#     updated_checkpoint = crud.update_checkpoint(db=db, checkpoint=db_checkpoint, checkpoint_update=checkpoint)
#     return updated_checkpoint

# @router.put("/shipping/{shipping_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
# def update_shipping(shipping_id: int, shipping: schemas.ShippingUpdate, db: db_dependecy):
#     db_shipping = crud.get_shipping_by_id(db=db, shipping_id=shipping_id)
#     if not db_shipping:
#         raise HTTPException(status_code=404, detail="Shipping not found")
#     updated_shipping = crud.update_shipping(db=db, shipping=db_shipping, shipping_update=shipping)
#     return updated_shipping

# @router.put("/wet_leaves/{wet_leaves_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
# def update_wet_leaves(wet_leaves_id: int, wet_leaves: schemas.WetLeavesUpdate, db: db_dependecy):
#     db_wet_leaves = crud.get_wet_leaves_by_id(db=db, wet_leaves_id=wet_leaves_id)
#     if not db_wet_leaves:
#         raise HTTPException(status_code=404, detail="Wet Leaves not found")
#     updated_wet_leaves = crud.update_wet_leaves(db=db, wet_leaves=db_wet_leaves, wet_leaves_update=wet_leaves)
#     return updated_wet_leaves

# @router.put("/dry_leaves/{dry_leaves_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
# def update_dry_leaves(dry_leaves_id: int, dry_leaves: schemas.DryLeavesUpdate, db: db_dependecy):
#     db_dry_leaves = crud.get_dry_leaves_by_id(db=db, dry_leaves_id=dry_leaves_id)
#     if not db_dry_leaves:
#         raise HTTPException(status_code=404, detail="Dry Leaves not found")
#     updated_dry_leaves = crud.update_dry_leaves(db=db, dry_leaves=db_dry_leaves, dry_leaves_update=dry_leaves)
#     return updated_dry_leaves

# @router.put("/flour/{flour_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
# def update_flour(flour_id: int, flour: schemas.FlourUpdate, db: db_dependecy):
#     db_flour = crud.get_flour_by_id(db=db, flour_id=flour_id)
#     if not db_flour:
#         raise HTTPException(status_code=404, detail="Flour not found")
#     updated_flour = crud.update_flour(db=db, flour=db_flour, flour_update=flour)
#     return updated_flour

@router.delete("/packages/{package_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
def delete_package(package_id: int, db: db_dependecy):
    db_package = crud.get_package_by_id(db=db, package_id=package_id)
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")
    crud.delete_package(db=db, package=db_package)
    return JSONResponse(content={"message": "Package deleted successfully"})

@router.delete("/checkpoints/{checkpoint_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
def delete_checkpoint(checkpoint_id: int, db: db_dependecy):
    db_checkpoint = crud.get_checkpoint_by_id(db=db, checkpoint_id=checkpoint_id)
    if not db_checkpoint:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    crud.delete_checkpoint(db=db, checkpoint=db_checkpoint)
    return JSONResponse(content={"message": "Checkpoint deleted successfully"})

@router.delete("/shipping/{shipping_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
def delete_shipping(shipping_id: int, db: db_dependecy):
    db_shipping = crud.get_shipping_by_id(db=db, shipping_id=shipping_id)
    if not db_shipping:
        raise HTTPException(status_code=404, detail="Shipping not found")
    crud.delete_shipping(db=db, shipping=db_shipping)
    return JSONResponse(content={"message": "Shipping deleted successfully"})

@router.delete("/wet_leaves/{wet_leaves_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
def delete_wet_leaves(wet_leaves_id: int, db: db_dependecy):
    db_wet_leaves = crud.get_wet_leaves_by_id(db=db, wet_leaves_id=wet_leaves_id)
    if not db_wet_leaves:
        raise HTTPException(status_code=404, detail="Wet Leaves not found")
    crud.delete_wet_leaves(db=db, wet_leaves=db_wet_leaves)
    return JSONResponse(content={"message": "Wet Leaves deleted successfully"})

@router.delete("/dry_leaves/{dry_leaves_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
def delete_dry_leaves(dry_leaves_id: int, db: db_dependecy):
    db_dry_leaves = crud.get_dry_leaves_by_id(db=db, dry_leaves_id=dry_leaves_id)
    if not db_dry_leaves:
        raise HTTPException(status_code=404, detail="Dry Leaves not found")
    crud.delete_dry_leaves(db=db, dry_leaves=db_dry_leaves)
    return JSONResponse(content={"message": "Dry Leaves deleted successfully"})

@router.delete("/flour/{flour_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
def delete_flour(flour_id: int, db: db_dependecy):
    db_flour = crud.get_flour_by_id(db=db, flour_id=flour_id)
    if not db_flour:
        raise HTTPException(status_code=404, detail="Flour not found")
    crud.delete_flour(db=db, flour=db_flour)
    return JSONResponse(content={"message": "Flour deleted successfully"})

@router.delete("/users/{user_id}", dependencies=[Depends(role_access(RoleEnum.admin))])
def delete_user(user_id: int, db: db_dependecy):
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db=db, user=db_user)
    return JSONResponse(content={"message": "User deleted successfully"})


