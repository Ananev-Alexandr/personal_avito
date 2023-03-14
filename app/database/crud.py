from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.schemas import user_schemas, adv_schemas
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
    

def create_advertisement(db: Session, adv: adv_schemas.AdvIn, user_id: int):
    db_adv = models.Advertisements(
        user_id=user_id,
        content=adv.content,
    )
    db.add(db_adv)
    db.commit()
    db.refresh(db_adv)
    return db_adv


def get_all_adv(db: Session):
    get_adv = db.query(models.Advertisements).all()
    return get_adv


def info_about_adv(db: Session, id: int):
    get_adv = db.query(models.Advertisements).\
        filter(models.Advertisements.id == id).one_or_none()
    if get_adv:
        return get_adv
    raise HTTPException(status_code=404, detail="Id not found")


def delete_adv(id: int, user_id: int, db: Session):
    find_adv = db.query(models.Advertisements).\
        filter(
            models.Advertisements.id == id,
            models.Advertisements.user_id == user_id
                ).one_or_none()
    if find_adv:
        adv = db.query(models.Advertisements).filter(models.Advertisements.id == id).first()
        db.delete(adv)
        db.commit()
        return {"message": "Success delete!"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Its not your post, post not found"
                )
        
def post_a_feedback(feedback, user_id: int, db: Session):
    find_feedback = db.query(models.Feedback).\
        filter(models.Feedback.advertisement_id == feedback.advertisement_id).\
            filter(models.Feedback.user_id == user_id).one_or_none()
    if not find_feedback:
        fb = models.Feedback(
        user_id=user_id,
        message=feedback.message,
        rate=feedback.rate,
        advertisement_id=feedback.advertisement_id
    )
        db.add(fb)
        db.commit()
        return {"message": "Success!"}
    else:
        raise HTTPException(
            status_code=403,
            detail="You have already left a feedback"
                )