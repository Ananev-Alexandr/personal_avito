from datetime import date, datetime
from typing import Union

from fastapi import Path
from pydantic import BaseModel


class AdvIn(BaseModel):
    content: str
    group_id: int
    title: str
    price: int


class AdvDB(AdvIn):
    id: int
    date_of_publication: datetime

    class Config:
        orm_mode = True


class FilterAdv(BaseModel):
    content: Union[str, None] = None
    group_id: Union[int, None] = 1
    title: Union[str, None] = None

    class Config:
        orm_mode = True


class FeedbackIn(BaseModel):
    advertisement_id: int
    message: str
    rate: int = Path(title="int", gt=1, le=10)


class FeedbackDB(FeedbackIn):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class FindFB(BaseModel):
    id:int
    message: str
    rate: int
    advertisement_id: int
    user_id: int
    
    class Config:
        orm_mode = True


class DateFilter(BaseModel):
    start_date: Union[date, None] = None
    end_date: Union[date, None] = None


class SortAdv(BaseModel):
    group_by: Union[str, None] = "asc"
    sort_by: Union[str, None] = "date_of_publication"


class FilterAndSortAdv(BaseModel):
    filters: Union[FilterAdv, None] = None
    group: Union[SortAdv, None] = None


class ComplaintIn(BaseModel):
    advertisement_id: int
    message: str

    class Config:
        orm_mode = True
        
class ComplaintOut(BaseModel):
    advertisement_id: int
    message: str
    user_id: int

    class Config:
        orm_mode = True