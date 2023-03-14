from pydantic import BaseModel
from datetime import datetime


class AdvIn(BaseModel):
    content: str


class AdvDB(AdvIn):
    id: int
    date_of_publication: datetime

    class Config:
        orm_mode = True