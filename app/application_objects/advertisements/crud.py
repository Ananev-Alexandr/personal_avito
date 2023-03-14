from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas import adv_schemas
from app.database import models


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
        find_feedback = db.query(models.Feedback).\
            filter(models.Feedback.advertisement_id == id).all()
        return [get_adv, find_feedback]
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