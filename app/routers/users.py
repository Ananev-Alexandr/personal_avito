from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db_connect import get_db
from app.database import crud
from app.schemas import user_schemas
from app.database.db import Base, engine

Base.metadata.create_all(bind=engine)


router = APIRouter(tags=["users"])


@router.get("/")
async def hello() -> dict:
    return {"Hello": "World"}


@router.post("/users/", response_model=user_schemas.UserOut)
async def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)