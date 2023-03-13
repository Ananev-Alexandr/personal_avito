from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.schemas import user_schemas
from app.database import models


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def verify_password(plain_password, hashed_password) -> bool:
    eq_pass = pwd_context.verify(plain_password, hashed_password)
    return eq_pass


def get_password_hash(password) -> str:
    hash = pwd_context.hash(password)
    return hash


def create_user(db: Session, user: user_schemas.UserCreate):
    db_user = models.User(
        password=get_password_hash(user.password),
        first_name=user.first_name,
        second_name=user.second_name,
        login=user.login,
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="This username already exists, please use another one"
                )