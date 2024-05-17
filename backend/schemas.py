from typing import Optional

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
    centra_id: int


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


class CheckpointDataBase(BaseModel):

    shipping_id: int
    total_packages: int

class CheckpointDataRecord(CheckpointDataBase):

    arrival_date: date
    note : Optional[str] = None


class CheckpointData(CheckpointDataRecord):

    id: int
    

    class Config:
        orm_mode = True

class centraNotification(BaseModel):

    id: int
    user_id: int

class centraNotificationMsg(centraNotification):
    msg: str

class centraNotificationData(centraNotification):

    id: int
    user_id: int

    class Config:
        orm_mode = True

class guardHarborNotification(BaseModel):

    id: int
    user_id: int

class guardHarborNotificationMsg(guardHarborNotification):
    msg: str

class guardHarborNotificationData(guardHarborNotification):
    
        id: int
        user_id: int
    
        class Config:
            orm_mode = True
            
class ReceptionPackageBase(BaseModel):
    package_id: str
    total_packages_received: int
    weight: float
    centra_id: int

class ReceptionPackageReceival(ReceptionPackageBase):
    receival_date: date

class ReceptionPackages(ReceptionPackageBase):
    id:int
    package_id: str
    centra_id: int

    class Config:
        orm_mode = True
