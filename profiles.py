from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Annotated, Optional

from database import SessionLocal
from models import Users
from auth import get_current_user

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class UserProfile(BaseModel):
    username: str
    centra_unit: Optional[int]
    role: str
    email: str

# Endpoint to get the current logged-in user's username


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(current_user: Users = Depends(get_current_user)):
    return {"username": current_user.username, "centra_unit": current_user.centra_unit, "role": current_user.role, "email": current_user.email}
