from typing import Optional

from pydantic import BaseModel
from datetime import date, timedelta


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


class DateRecord(BaseModel):
    date: date

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
        from_attributes = True


class DryLeavesBase(BaseModel):

    weight: float


class DryLeavesRecord(DryLeavesBase):
    dried_date: date


class DryLeaves(DryLeavesBase):

    id: int
    dried_date: date

    class Config:
        from_attributes = True


class FlourBase(BaseModel):

    weight: float


class FlourRecord(FlourBase):
    floured_date: date


class Flour(FlourBase):

    id: int
    floured_date: date

    class Config:
        from_attributes = True

# class FlourRequest():

#     id: Optional[int]
#     date: Optional[date]
#     interval: Optional[timedelta]
#     mode: Optional[int]

class packageRecord(BaseModel):
    
    centra_id: int
    weight: float
    shipping_id: Optional[int]=None
    status: int=0

class ShippingInfoRecord(BaseModel):

    packages: list[int]
    total_packages: int
    total_weight: float
    expedition: str
    departure_date: date
    estimated_time: timedelta

class ShippingDataRecord(BaseModel):

    id: int
    expedition_id: int


class ShippingDepature(ShippingDataRecord):
    departure_date: date


class ShippingData(ShippingDataRecord):

    id: int
    expedition_id: int

    class Config:
        from_attributes = True
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
        from_attributes = True

class CentraNotification(BaseModel):

    id: int
    user_id: int

class CentraNotificationMsg(CentraNotification):
    msg: str

class CentraNotificationData(CentraNotification):

    id: int
    user_id: int

    class Config:
        from_attributes = True

class GuardHarborNotification(BaseModel):

    id: int
    user_id: int

class GuardHarborNotificationMsg(GuardHarborNotification):
    msg: str

class GuardHarborNotificationData(GuardHarborNotification):
    
        id: int
        user_id: int
    
        class Config:
            from_attributes = True
            
class ReceptionPackageBase(BaseModel):
    package_id: str
    total_packages_received: int
    weight: float
    centra_id: int
    receival_date: date

class ReceptionPackageRecord(ReceptionPackageBase):
    pass
    

class ReceptionPackage(ReceptionPackageBase):
    id:int

    class Config:
        from_attributes = True

class ReceptionPackageReceival(ReceptionPackageBase):
    receival_date: date