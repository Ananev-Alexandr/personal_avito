from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from app.database.db import Base


class Role(Base):
    __tablename__ = "role_table"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    user = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String)
    second_name = Column(String)
    date_of_registration = Column(DateTime, default=datetime.now)
    role_id = Column(ForeignKey("role_table.id"), default=1)
    time_zone = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

    role = relationship("Role", back_populates="user")
    complaint_user = relationship("Complaint", back_populates="user")


class Advertisements(Base):
    __tablename__ = "advertisement_table"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    date_of_publication = Column(String, default=datetime.now)
    group_id = Column(
        Integer,
        ForeignKey("advertisement_group_table.id"),
        nullable=False
        )
    price = Column(Integer, nullable=False)

    fb = relationship("Feedback", back_populates="adv")
    adv_g = relationship("AdvertisementsGroup", back_populates="advg")
    complaint_adv = relationship("Complaint", back_populates="adv")


class AdvertisementsGroup(Base):
    __tablename__ = "advertisement_group_table"

    id = Column(Integer, primary_key=True)
    group_name = Column(String, nullable=False)

    advg = relationship("Advertisements", back_populates="adv_g")


class Feedback(Base):
    __tablename__ = "feedback_table"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    advertisement_id = Column(
        Integer,
        ForeignKey("advertisement_table.id"),
        nullable=False,
        primary_key=True
            )
    user_id = Column(
        Integer,
        ForeignKey("user_table.id"),
        nullable=False,
        primary_key=True
            )
    message = Column(String, nullable=False)
    rate = Column(Integer)

    adv = relationship("Advertisements", back_populates="fb")


class Complaint(Base):
    __tablename__ = "complaint_table"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    advertisement_id = Column(
        Integer,
        ForeignKey("advertisement_table.id"),
        nullable=False,
        primary_key=True
            )
    user_id = Column(
        Integer,
        ForeignKey("user_table.id"),
        nullable=False,
        primary_key=True
            )
    message = Column(String, nullable=False)
    date_of_create = Column(String, default=datetime.now)

    user = relationship("User", back_populates="complaint_user")
    adv = relationship("Advertisements", back_populates="complaint_adv")
