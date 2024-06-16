from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
from models import Users
from auth import get_current_user
from roles_enum import RoleEnum

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UpdateProfileRequest(BaseModel):
    username: str
    email: EmailStr
    new_password: Optional[str]
    confirm_password: Optional[str]
    centra_unit: Optional[str]


@router.put("/", status_code=status.HTTP_200_OK)
async def update_profile(
    update_profile_request: UpdateProfileRequest,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(Users).filter(Users.id == current_user.id).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.username = update_profile_request.username
        user.email = update_profile_request.email

        if update_profile_request.new_password and update_profile_request.confirm_password:
            if update_profile_request.new_password != update_profile_request.confirm_password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Passwords do not match"
                )
            user.hashed_password = bcrypt_context.hash(
                update_profile_request.new_password)
        if user.role == RoleEnum.centra:
            user.centra_unit = update_profile_request.centra_unit

        db.commit()

        # Refresh user to get updated details
        db.refresh(user)

        return {
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "centra_unit": user.centra_unit
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )
