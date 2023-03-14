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
    if info_about_user_for_login(db, user.login):
        raise HTTPException(status_code=404, detail="Login already used")
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
            detail="Incorrectly filled fields"
                )
        
def info_about_user(db: Session, id: int):
    db_user = db.query(models.User).\
        filter(models.User.id == id).one_or_none()
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="Id not found")

def info_about_user_for_login(db: Session, login: str):
    db_user = db.query(models.User).\
        filter(models.User.login == login).one_or_none()
    if db_user:
        return db_user


def ban(id: int, db: Session):
    interesting_user = db.query(models.User).filter(models.User.id == id)
    if interesting_user.one_or_none() is None:
        raise HTTPException(status_code=404, detail="Id not found")
    elif interesting_user.filter(models.User.active == True).one_or_none():
        interesting_user = interesting_user.update({models.User.active: False})
        db.commit()
        return {"message": "Success ban!"}
    else:
        interesting_user = interesting_user.update({models.User.active: True})
        db.commit()
        return {"message": "Success unban!"}


def give_root_admin(id: int, db: Session):
    interesting_user = db.query(models.User).filter(models.User.id == id)
    if interesting_user.one_or_none() is None:
        raise HTTPException(status_code=404, detail="Id not found")
    elif interesting_user.filter(models.User.active == False).one_or_none():
        raise HTTPException(status_code=404, detail="User in ban")
    elif interesting_user.one_or_none().role_id == 2:
        raise HTTPException(status_code=404, detail="The user is already an admin")
    elif interesting_user.one_or_none():
        interesting_user = interesting_user.update({models.User.role_id: 2})
        db.commit()
        return {"message": "You have given admin rights!"}
    else:
        raise HTTPException(status_code=404, detail="User in ban")