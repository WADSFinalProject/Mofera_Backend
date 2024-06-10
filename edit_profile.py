from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import SessionLocal
from models import Users
from auth import get_current_user, db_dependency
from roles_enum import RoleEnum
from pydantic.types import constr
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UpdateProfileRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=500)
    email: EmailStr
    new_password: Optional[str] = Field(None, min_length=6, max_length=500)
    confirm_password: Optional[str] = Field(None, min_length=6, max_length=500)


@router.put("/edit", status_code=status.HTTP_200_OK)
async def update_profile(
    update_request: UpdateProfileRequest,
    db: Session = Depends(db_dependency),
    current_user: Users = Depends(get_current_user)
):

    # Ensure new password and confirm password match
    if update_request.new_password and update_request.new_password != update_request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="New passwords do not match")

    # Update user details
    current_user.username = update_request.username
    current_user.email = update_request.email
    if current_user.role == RoleEnum.centra:
        current_user.centra_unit = update_request.centra_unit

    if update_request.new_password:
        current_user.hashed_password = bcrypt_context.hash(
            update_request.new_password)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {
        "username": current_user.username,
        "email": current_user.email,
        "centra_unit": current_user.centra_unit,
        "role": current_user.role
    }
