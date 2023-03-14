from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.db_connect import get_db
from app.database import crud
from app.schemas import user_schemas
from app.database.db import Base, engine
from app.security import services
from app.security.schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import os


router = APIRouter(tags=["users"])


@router.get("/")
async def hello(current_user=Depends(services.get_current_user)) -> dict:
    return {"Hello": "World"}


@router.post("/users/", response_model=user_schemas.UserOut)
async def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@router.put("/ban/{id}")
async def ban(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
    ):
    return crud.ban(db=db, id=id, current_user=current_user)


@router.post("/token", response_model=Token, include_in_schema=False)
async def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
        ):
    user = services.login(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
    access_token = services.create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
