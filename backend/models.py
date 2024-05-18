from database import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, func, DateTime, Boolean,  Enum as SQLEnum, Enum
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

    refresh_tokens = relationship(
        "RefreshToken", back_populates="users", order_by="RefreshToken.expires_at.desc()")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(length=7000), index=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    expires_at = Column(DateTime)

    users = relationship("Users", back_populates="refresh_tokens")

# Centra, etc


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True)
    shipping_id = Column(Integer, ForeignKey("shipping.id"))
    receiver_name = Column(String)
    pickup_time = Column(Date)

    shipping = relationship("Shipping", backref="appointment")


class Centra(Base):
    __tablename__ = "centra"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    collection_id = Column(Integer, ForeignKey("collection.id"))
    package_data_id = Column(Integer, ForeignKey("package_data.id"))
    # reception_package_id = Column(Integer, ForeignKey("reception_package.id"))

    collection_centra = relationship("Collection", backref="centra", foreign_keys=[collection_id])
    package_data_centra = relationship("PackageData", backref="centra", foreign_keys=[package_data_id])
    # reception_package_centra = relationship(
    #     "ReceptionPackage", backref="centra", foreign_keys=[reception_package_id])


class CheckpointData(Base):
    __tablename__ = "checkpoint_data"

    id = Column(Integer, primary_key=True, index=True)
    arrival_date = Column(Date)
    total_packages = Column(Integer)
    shipping_id = Column(Integer, ForeignKey("shipping.id"))
    note = Column(String(length=500))

    shipping = relationship("Shipping", backref="shipping_collection")


class Expedition(Base):
    __tablename__ = "expedition"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class PackageData(Base):
    __tablename__ = "package_data"

    id = Column(Integer, primary_key=True, index=True)
    shipping_collection_id = Column(Integer)
    centra_id = Column(Integer, ForeignKey("centra.id"))
    weight = Column(Float)

    centra_owner = relationship("Centra", backref="package_data", foreign_keys=[centra_id])


class RescaledPackageData(Base):
    __tablename__ = "rescaled_package_data"

    id = Column(Integer, primary_key=True, index=True)
    package_id = Column(Integer, ForeignKey("package_data.id"))
    rescaled_weight = Column(Float)

    original_package = relationship(
        "PackageData", backref="rescaled_package_data")


class ReceptionPackage(Base):
    __tablename__ = "reception_package"

    id = Column(Integer, primary_key=True, index=True)
    package_id = Column(Integer, ForeignKey("package_data.id"))
    final_weight = Column(Float)
    receival_date = Column(Date)
    centra_id = Column(Integer, ForeignKey("centra.id"))

    source_centra = relationship("Centra", backref="reception_package", foreign_keys=[centra_id])
    original_package = relationship("PackageData", backref="reception_package", foreign_keys=[package_id])


class Shipping(Base):
    __tablename__ = "shipping"

    id = Column(Integer, primary_key=True, index=True)
    departure_date = Column(Date)
    expedition_id = Column(Integer, ForeignKey("expedition.id"))
    guard_harbor_dest_id = Column(Integer, ForeignKey("guard_harbor.id"))

    expedition = relationship("Expedition", backref="shipping")
    guard_harbor = relationship("GuardHarbor", backref="shipping")


class GuardHarbor(Base):
    __tablename__ = "guard_harbor"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    checkpoint_id = Column(Integer, ForeignKey("checkpoint_data.id"))

    checkpoint = relationship("CheckpointData", backref="guard_harbor")


class Collection(Base):
    __tablename__ = "collection"

    id = Column(Integer, primary_key=True, index=True)
    retrieval_date = Column(Date)
    weight = Column(Float)
    centra_id = Column(Integer, ForeignKey("centra.id"))


class Dry(Base):
    __tablename__ = "dry"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float)
    dried_date = Column(Date)


class Flour(Base):
    __tablename__ = "flour"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float)
    floured_date = Column(Date)

class CentraNotification(Base):
    __tablename__ = "centra_notification"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Integer)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("Users", backref="centra_notification")

class GuardHarborNotification(Base):
    __tablename__ = "guard_harbor_notification"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("Users", backref="guard_harbor_notification")

class ReceptionPackage(Base):
    __tablename__ = 'reception_packages'
    id = Column(Integer, primary_key=True, index=True)
    package_id = Column(String, ForeignKey("package_data.id"))
    total_packages_received = Column(Integer)
    weight = Column(Float)
    receival_date = Column(Date)
    centra_id = Column(Integer, ForeignKey("centra.id"))

    centra = relationship("Centra", backref="reception_packages", foreign_keys=[centra_id])
    package = relationship("PackageData", backref="reception_packages", foreign_keys=[package_id])