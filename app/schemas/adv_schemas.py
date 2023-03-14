from pydantic import BaseModel
from datetime import datetime
from fastapi import Path


class AdvIn(BaseModel):
    content: str


class AdvDB(AdvIn):
    id: int
    date_of_publication: datetime

    class Config:
        orm_mode = True


class FeedbackIn(BaseModel):
    advertisement_id: int
    message: str
    rate: int = Path(title="int",gt=1,le=10)
    
class FeedbackDB(FeedbackIn):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True