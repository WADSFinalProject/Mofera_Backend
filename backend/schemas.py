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
    weight: float


class WetLeavesRecord(WetLeavesBase):
    retrieval_date: date


class WetLeaves(WetLeavesBase):

    id: int
    retrieval_date: date
    centra_id: int

    class Config:
        orm_mode = True


class DryLeavesBase(BaseModel):

    weight: float


class DryLeavesRecord(DryLeavesBase):
    exp_date: date


class DryLeaves(DryLeavesBase):

    id: int
    exp_date: date

    class Config:
        orm_mode = True


class FlourBase(BaseModel):

    weight: float


class FlourRecord(FlourBase):
    finish_time: date


class Flour(FlourBase):

    id: int
    finish_time: date

    class Config:
        orm_mode = True


class ShippingDataRecord(BaseModel):

    id: int
    expedition_id: int


class ShippingDepature(ShippingDataRecord):
    departure_date: date


class ShippingData(ShippingDataRecord):

    id: int
    expedition_id: int

    class Config:
        orm_mode = True
# Checkpoint


class CheckpointDataRecord(BaseModel):

    package_id: int
    shipping_id: int
    total_received_package: int


class CheckpointData(CheckpointDataRecord):

    id: int
    arrival_date: date

    class Config:
        orm_mode = True
