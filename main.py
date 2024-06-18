

import models
import auth
import centra
import guard_harbor
import usersmanagement
import profiles
import edit_profile
import xyz
import uvicorn
import forget_password
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request, status
import admin
# from apscheduler.schedulers.background import BackgroundScheduler


from sqlalchemy.orm import Session
from typing import List, Annotated
from pydantic import BaseModel, Field
from database import SessionLocal, engine
# from datetime import date
# from models import Users
# import crud

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app = FastAPI()

router = APIRouter()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Oops! That resource does not exist."},
        )
    else:
        content = {"message": exc.detail}
        return JSONResponse(status_code=exc.status_code, content=content)
    return await request.app.default_exception_handler(request, exc)


app.include_router(auth.router)
app.include_router(centra.router)
app.include_router(guard_harbor.router)
app.include_router(usersmanagement.router)
app.include_router(profiles.router)
app.include_router(edit_profile.router)
app.include_router(forget_password.router)
app.include_router(xyz.router)
app.include_router(admin.router)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "https://mofera-frontend-six.vercel.app"
    # add other origins here


]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# @app.on_event("startup")
# def startup_event():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(check_expired_packages, 'interval', minutes=60)
#     scheduler.start()

# def check_expired_packages():
#     db = SessionLocal()
#     try:
#         expired_packages = crud.check_package_expiry(db)
#         if expired_packages:
#             print(f"Updated {len(expired_packages)} expired packages.")
#     finally:
#         db.close()

# @app.get("/check_expired_packages/")
# def manual_check_expired_packages(db: Session = Depends(get_db)):
#     expired_packages = crud.check_and_update_expired_packages(db)
#     return {"updated_packages": len(expired_packages)}

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: None, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
