from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    first_name: str
    second_name: str
    password: str


class UserOut(BaseModel):
    first_name: str
    second_name: str
    id: int
    date_of_registration: datetime
    role_id: int
    time_zone: datetime
    active: bool

    class Config:
        orm_mode = True
