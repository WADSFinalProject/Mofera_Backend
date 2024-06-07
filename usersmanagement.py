from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging

from database import get_db
from models import Users
from pydantic import BaseModel
from roles_enum import RoleEnum

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/users",
    tags=["users"]
)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: RoleEnum


@router.get("/userinfo", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(
            Users.id,
            Users.username,
            Users.email,
            Users.role
        ).all()

        return users

    except SQLAlchemyError as e:
        logger.error(f"Error retrieving users: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve users")
    except Exception as e:
        logger.error(f"Unexpected error retrieving users: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error")

# delete user functionality


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return user

    except SQLAlchemyError as e:
        logger.error(f"Error deleting user: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete user")
    except Exception as e:
        logger.error(f"Unexpected error deleting user: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error")
