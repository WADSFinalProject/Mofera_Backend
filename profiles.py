from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Annotated

from database import SessionLocal
from models import Users
from auth import get_current_user  # Assuming get_current_user is in auth.py

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)

# Dependency to get DB Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# Pydantic Model for the response


class UserProfile(BaseModel):
    username: str

# Endpoint to get the current logged-in user's username


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(current_user: Users = Depends(get_current_user)):
    return {"username": current_user.username}
