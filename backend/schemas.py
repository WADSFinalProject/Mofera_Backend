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
    weight: int

class WetLeavesRecord(WetLeavesBase):
    retrieval_date: date

class WetLeaves(WetLeavesBase):
    
    id: int
    retrieval_date: date
    centra_id: int

    class Config:
        orm_mode = True

# Checkpoint

class CheckpointDataRecord(BaseModel):

    id: int
    shipping_id: int
    total_received_package: int
    total_sent_package: int
    arrival_date: date
