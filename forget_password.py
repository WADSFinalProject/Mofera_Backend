# forget_password.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText

from database import SessionLocal
from models import Users
from auth import SECRET_KEY, ALGORITHM, get_current_user, get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Utility functions

def create_reset_token(user_id: int, expires_delta: timedelta = timedelta(hours=1)):
    encode = {"id": user_id}
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
        encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def send_reset_email(email: str, reset_link: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "moferanaturals@gmail.com"
    smtp_password = "ymky zdev bbgk opyb"

    msg = MIMEText(
        f'Hi,<br><br>Click on the link to reset your password: <a href="{reset_link}">{reset_link}</a>', 'html')
    msg['Subject'] = 'Password Reset'
    msg['From'] = smtp_user
    msg['To'] = email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, email, msg.as_string())

# Request models

class PasswordResetRequest(BaseModel):
    email: str


class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    @validator("confirm_password")
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError("Passwords do not match")
        return v

# Endpoints

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    user = current_user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    reset_token = create_reset_token(user.id)
    reset_link = f"https://mofera-frontend-six.vercel.app/resetpass?token={reset_token}"

    send_reset_email(user.email, reset_link)

    return {"message": "Password reset email sent"}

@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(request: PasswordReset, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Passwords match validation is handled by Pydantic validator
        user.hashed_password = bcrypt_context.hash(request.new_password)
        db.commit()

        return {"message": "Password reset successful"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
