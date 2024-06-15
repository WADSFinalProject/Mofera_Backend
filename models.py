from database import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, func, DateTime, Boolean, Enum as SQLEnum, Enum, Interval
from sqlalchemy.orm import relationship
from roles_enum import RoleEnum

# Autn, admin, user


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=500))
    password = Column(String(length=500))


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=500))
    email = Column(String(length=500), unique=True)
    hashed_password = Column(String(length=500))
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.centra, nullable=False)
    centra_unit = Column(String(length=500))
    is_active = Column(Boolean, default=True)  # New column for soft deletion
    refresh_tokens = relationship(
        "RefreshToken", back_populates="users", cascade="all, delete")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(length=7000), index=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    expires_at = Column(DateTime)

    users = relationship("Users", back_populates="refresh_tokens")


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True)
    shipping_id = Column(Integer, ForeignKey("shipping.id"))
    receiver_name = Column(String(500))
    pickup_time = Column(Date)

    shipping = relationship("Shipping", backref="appointment")


class Centra(Base):
    __tablename__ = "centra"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(500))
    # reception_package_id = Column(Integer, ForeignKey("reception_package.id"))

    # reception_package_centra = relationship(
    #     "ReceptionPackage", backref="centra", foreign_keys=[reception_package_id])


class CheckpointData(Base):
    __tablename__ = "checkpoint_data"

    id = Column(Integer, primary_key=True, index=True)
    arrival_datetime = Column(DateTime)
    total_packages = Column(Integer)
    shipping_id = Column(Integer, ForeignKey("shipping.id"))
    note = Column(String(length=500))

    shipping = relationship("Shipping", backref="shipping_collection")


class Expedition(Base):
    __tablename__ = "expedition"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500))


class PackageData(Base):
    __tablename__ = "package_data"

    id = Column(Integer, primary_key=True, index=True)
    centra_id = Column(Integer, ForeignKey("centra.id"))
    weight = Column(Float)
    shipping_id = Column(Integer, ForeignKey("shipping.id"), nullable=True)
    status = Column(Integer, default=0)
    received_date = Column(Date, nullable=True)
    reception_id = Column(Integer, nullable=True)
    exp_date = Column(Date, nullable=True)

    centra_owner = relationship(
        "Centra", backref="package_data", foreign_keys=[centra_id])
    shipping = relationship(
        "Shipping", backref="packages", foreign_keys=[shipping_id])


class RescaledPackageData(Base):
    __tablename__ = "rescaled_package_data"

    id = Column(Integer, primary_key=True, index=True)
    package_id = Column(Integer, ForeignKey("package_data.id"))
    rescaled_weight = Column(Float)
    materials_to_cover = Column(String(500))

    original_package = relationship(
        "PackageData", backref="rescaled_package_data")


class Shipping(Base):
    __tablename__ = "shipping"

    id = Column(Integer, primary_key=True, index=True)
    departure_datetime = Column(DateTime)
    total_weight = Column(Float)
    total_packages = Column(Integer)
    expedition = Column(String(500))
    centra_id = Column(Integer)
    # expedition_id = Column(Integer, ForeignKey("expedition.id"))

    # expedition = relationship("Expedition", backref="shipping")


class GuardHarbor(Base):
    __tablename__ = "guard_harbor"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(500))
    checkpoint_id = Column(Integer, ForeignKey("checkpoint_data.id"))

    checkpoint = relationship("CheckpointData", backref="guard_harbor")


class Collection(Base):
    __tablename__ = "collection"

    id = Column(Integer, primary_key=True, index=True)
    retrieval_date = Column(Date)
    weight = Column(Float)
    centra_id = Column(Integer, ForeignKey("centra.id"))


class Wet(Base):
    __tablename__ = "wet"

    id = Column(Integer, primary_key=True, index=True)
    retrieval_date = Column(Date)
    washed_datetime = Column(DateTime, nullable=True)
    dried_datetime = Column(DateTime, nullable=True)
    weight = Column(Float)
    centra_id = Column(Integer, ForeignKey("centra.id"))

    # centra = relationship("Centra", backref="wet")


class Dry(Base):
    __tablename__ = "dry"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float)
    dried_date = Column(Date)
    floured_datetime = Column(DateTime, nullable=True)
    centra_id = Column(Integer)


class Flour(Base):
    __tablename__ = "flour"

    id = Column(Integer, primary_key=True, index=True)
    dried_date = Column(Date)
    floured_date = Column(Date)
    weight = Column(Float)
    centra_id = Column(Integer)


class CentraNotification(Base):
    __tablename__ = "centra_notification"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(500))
    date = Column(DateTime)
    centra_id = Column(Integer)


class GuardHarborNotification(Base):
    __tablename__ = "guard_harbor_notification"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(500))
    date = Column(DateTime)
    centra_id = Column(Integer)


class ReceptionPackage(Base):
    __tablename__ = "reception_packages"
    id = Column(Integer, primary_key=True, index=True)
    package_id = Column(Integer, ForeignKey("package_data.id"))
    total_packages_received = Column(Integer)
    weight = Column(Float)
    receival_date = Column(Date)
    centra_id = Column(Integer, ForeignKey("centra.id"))

    centra = relationship(
        "Centra", backref="reception_packages", foreign_keys=[centra_id])
    package = relationship(
        "PackageData", backref="reception_packages", foreign_keys=[package_id])
