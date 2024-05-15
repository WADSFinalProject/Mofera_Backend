from pydantic import BaseModel
from datetime import date

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

class WetLeavesBase(BaseModel):
    retrieval_date: date
    weight: int
    centra_id: int

class WetLeaves(WetLeavesBase):
    id: int

    class Config:
        orm_mode = True