from typing import Optional

from pydantic import BaseModel
from datetime import date, timedelta, datetime
from roles_enum import RoleEnum



class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


class VerificationEmailRequest(BaseModel):
    email: str
    verification_link: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    role: Optional[RoleEnum]
    centra_unit: Optional[str]

    class Config:
        orm_mode = True

class DatetimeRecord(BaseModel):
    datetime: datetime

class DateRecord(BaseModel):
    date: date

class CentraBase(BaseModel):
    location: str

class CentraRecord(CentraBase):
    pass

class CollectionBase(BaseModel):
    weight: float

class CollectionRecord(CollectionBase):
    retrieval_datetime: datetime

class WetLeavesBase(BaseModel):
    weight: float


class WetLeavesRecord(WetLeavesBase):
    retrieval_date: date


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
    dried_date: datetime

    class Config:
        from_attributes = True

class DryLeavesMobile(DateRecord):

    interval: str

class FlourBase(BaseModel):

    weight: float


class FlourRecord(FlourBase):
    dried_date: date
    floured_date: date


class Flour(FlourBase):

    id: int
    floured_date: date

    class Config:
        from_attributes = True

class packageRecord(BaseModel):
    
    weight: float
    shipping_id: Optional[int]=None
    status: int =0
    exp_date: date

class PackageCreate(packageRecord):
    pass

class PackageUpdate(packageRecord):
    status: int

class Package(packageRecord):
    
        id: int
        status: int
        created_datetime: Optional[datetime] = None
    
        class Config:
            from_attributes = True

class ShippingInfoRecord(BaseModel):

    packages: list[int]
    total_packages: int
    total_weight: float
    expedition: str
    departure_datetime: datetime
    eta_datetime: datetime

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

    arrival_datetime: datetime
    package_ids: list[int]
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

class RescaledRecord(BaseModel):
    weight: float
    material: str

class ReceptionPackageBase(BaseModel):
    package_id: list[int]
    total_packages_received: int
    weight: float
    centra_id: str
    receival_datetime: datetime
    guard_harbor_name: str
    xyz_name: str
    description: str


class ReceptionPackageRecord(ReceptionPackageBase):
    pass
    

class ReceptionPackage(ReceptionPackageBase):
    id:int

    class Config:
        from_attributes = True

class ReceptionPackageReceival(ReceptionPackageBase):
    receival_datetime: datetime