from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.database.db import Base
from datetime import datetime
from sqlalchemy.orm import relationship



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



class Advertisements(Base):
    __tablename__ = "advertisement_table"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    content = Column(String, nullable=False)
    date_of_publication = Column(String, default=datetime.now)
    
    #TODO relationship
    fb = relationship("Feedback", back_populates="adv")
    


class Comments(Base):
    __tablename__ = "comment_table"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    advertisement_id = Column(Integer, ForeignKey("advertisement_table.id"), nullable=False)
    content = Column(String, nullable=False)
    date_of_create = Column(DateTime, default=datetime.now)
    
    
    #TODO relationship
    
    
class Feedback(Base):
    __tablename__ = "feedback_table"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    advertisement_id = Column(Integer, ForeignKey("advertisement_table.id"), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"), nullable=False, primary_key=True)
    message = Column(String, nullable=False)
    rate = Column(Integer)
    
    adv = relationship("Advertisements", back_populates="fb")
    
    