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


router = APIRouter(


    prefix="/auth",
    tags=["auth"]

)
SECRET_KEY = '194679e3j938492938382883dej3ioms998323ftu933@jd7233!'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
auth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


# pydantic models
class CreateUserRequest(BaseModel):

    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


class VerificationEmailRequest(BaseModel):
    email: str
    verification_link: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependecy = Annotated[Session, Depends(get_db)]


logger = logging.getLogger(__name__)


# Register endpoint
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependecy, create_user_request: CreateUserRequest):
    try:
        create_user_model = Users(
            username=create_user_request.username,
            email=create_user_request.email,
            hashed_password=bcrypt_context.hash(create_user_request.password),
        )
        db.add(create_user_model)
        db.commit()

        # verification link functionality will be completed later after admin page is created
        # its purpose is to send verification link to the user's email upon registration where when the user clicks
        # on the verification link, the user will be automacally assigned their role from the admin page

        """  verification_link = "https://your-verification-page-url.com"

            return {"message": "User created successfully", "verification_link": verification_link} """

    except SQLAlchemyError as e:
        logger.error(f"Error creating user: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")
    except Exception as e:
        logger.error(f"Unexpected error creating user: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error")


# This function generates a refresh token,
# which is used to obtain a new access token without requiring the user to log in again.
# For example, when the user session expires it regenrates the token

def create_refresh_token(user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {'id': user_id}
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
        encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# The following endpoint refreshes the access token using a provided refresh token
# Allows users to obtain a new access token without having to log in again,
#  extending user sessions and maintaining access to protected resources over time. now set to 24 hrs
@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Invalid refresh token")

        # Validate refresh token in the database
        db_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token, RefreshToken.user_id == user_id).first()
        if not db_token or db_token.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=401, detail="Refresh token expired")

        user = db.query(Users).filter(Users.id == user_id).first()
        new_access_token = create_user_token(
            user.username, user.email, user.id, timedelta(hours=24))

        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


# Login endpoint

# This endpoint handles user authentication and generates access and refresh tokens upon successful login.
# this token is used in the frontend for login
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password'
            )
        access_token = create_user_token(
            username=user.username,
            email=user.email,
            user_id=user.id,
            expires_delta=timedelta(hours=24)
        )
        refresh_token = create_refresh_token(user.id, timedelta(days=7))
        new_refresh_token = RefreshToken(
            token=refresh_token, user_id=user.id, expires_at=datetime.utcnow() +
            timedelta(days=7)
        )
        db.add(new_refresh_token)
        db.commit()
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
            'username': user.username
        }
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        raise HTTPException(
            status_code=500, detail="Unexpected error during login")


# This function verifies user credentials during the login process.
def authenticate_user(email: str, password: str, db):

    user = db.query(Users).filter(Users.email == email).first()
    if bcrypt_context.verify(password, user.hashed_password):
        return user
    return None


def create_user_token(username: str, email: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {'sub': username, 'email': email, 'id': user_id}
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
        encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# SendPulse,  third-party service which we can use its API to send emails

def send_verification_email(email: str, verification_link: str):
    try:
        # SendPulse API key
        api_key = "5304b71464544809aa6b02c5a111c936"
        url = "https://api.sendpulse.com/smtp/emails"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "html": f'<p>Click the following link to verify your email: <a href="{verification_link}">{verification_link}</a></p>',
            "subject": "Verify Your Email",
            # we need to change to our email as a sender
            "from": {"name": "Sender Name", "email": "abasiman15@gmail.com"},
            "to": [{"email": email}]
        }
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email:", str(e))


# Update the route to use the new send_verification_email function
@router.post("/send-verification-email", status_code=status.HTTP_202_ACCEPTED)
async def send_verification_email_endpoint(request: VerificationEmailRequest, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(
            send_verification_email, request.email, request.verification_link)
        return {"message": "Verification email sent successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to send verification email")
