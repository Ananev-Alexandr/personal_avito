from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas import adv_schemas
from app.database import models


def create_advertisement(db: Session, adv: adv_schemas.AdvIn, user_id: int):
    db_adv = models.Advertisements(
        user_id=user_id,
        title=adv.title,
        content=adv.content,
        group_id=adv.group_id
    )
    try:
        db.add(db_adv)
        db.commit()
        db.refresh(db_adv)
        return db_adv
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Incorrectly filled fields"
                )


def find_adv_for_id(db: Session, id: int):
    get_adv = db.query(models.Advertisements).\
        filter(models.Advertisements.id == id).one_or_none()
    return get_adv


def info_about_adv(db: Session, id: int):
    get_adv = find_adv_for_id(db=db, id=id)
    if get_adv:
        return get_adv
    raise HTTPException(status_code=404, detail="Id not found")


def feedback_interesting_adv(db: Session, id: int):
    find_feedback = db.query(models.Feedback).\
            filter(models.Feedback.advertisement_id == id).all()
    return find_feedback


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

        
def delete_feedback_advt_by_admin(feedback_id: int, db: Session):
    find_feedback = db.query(models.Feedback).\
        filter(models.Feedback.id == feedback_id)
    if find_feedback.one_or_none() is None:
        raise HTTPException(
            status_code=403,
            detail="Feedback not found"
                )
    find_feedback = find_feedback.one_or_none()
    try:
        db.delete(find_feedback)
        db.commit()
        return {"message": "Success delete!"}
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Incorrectly filled fields"
                )



def post_a_feedback(feedback, user_id: int, db: Session):
    if find_adv_for_id(db=db, adv=feedback.advertisement_id) is None:
        raise HTTPException(status_code=404, detail="Id not found")
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
        try:
            db.add(fb)
            db.commit()
            return {"message": "Success!"}
        except Exception:
            raise HTTPException(
                status_code=404,
                detail="Incorrectly filled fields"
                    )
            
def finde_feedback(adv_id: int, db: Session):
    adv = find_adv_for_id(db=db, id=adv_id)
    if adv is None:
        raise HTTPException(status_code=404, detail="Id not found")
    all_feedback_in_adv = db.query(models.Feedback).\
        filter(models.Feedback.advertisement_id == adv_id).all()
    return all_feedback_in_adv


def сhanging_the_group_adv(id: int, db: Session, new_group: int):
    adv = find_adv_for_id(db=db, id=id)
    if adv is None:
        raise HTTPException(status_code=404, detail="Id not found")
    db.query(models.Advertisements).\
        filter(models.Advertisements.id == id).update({models.Advertisements.group_id: new_group})
    try:
        db.commit()
        return {"message": "Success change!"}
    except Exception:
            raise HTTPException(
                status_code=404,
                detail="Incorrectly filled fields"
                    )
            
def get_all_adv(filter_and_sort, db: Session):
    schemas_filter, group_filters = validate_params(filter_and_sort)
    query = db.query(models.Advertisements)
    query = filter_adv(query, schemas_filter)
    query = sort_adv(query, group_filters)
    query = query.all()
    return query

    
    
def validate_params(dict_of_filter) -> dict:
    dict_of_filter = dict(dict_of_filter)
    if dict_of_filter.get("filters"):
        dict_filters = dict(dict_of_filter.get("filters"))
    if dict_of_filter.get("group"):
        group_filters = dict(dict_of_filter["group"])
    if dict_filters.get("publication_date"):
        dict_filters["publication_date"] = dict(
            dict_filters["publication_date"]
                )

    copy_filters = dict_filters.copy()
    for key, val in copy_filters.items():
        if val is None:
            del dict_filters[key]

    return dict_filters, group_filters

def filter_adv(query, dict_of_filter):
    association_table = {
        "id": models.Advertisements.id,
        "title": models.Advertisements.title,
        "content": models.Advertisements.content,
        "date_of_publication": models.Advertisements.date_of_publication
    }

    for key, val in dict_of_filter.items():
        if key == "id":
            query = query.filter(association_table[key] == val)
        elif key == "title":
            query = query.filter(association_table[key].ilike(f'%{val}%'))
        elif key == "content":
            query = query.filter(association_table[key].ilike(f'%{val}%'))
        elif key == "date_of_publication":
            date_range = dict(val)
            if date_range.get("start_date"):
                query = query.filter(
                    association_table[key] >= date_range["start_date"]
                        )
            if date_range.get("end_date"):
                query = query.filter(
                    association_table[key] <= date_range["end_date"]
                        )
       
    return query


def sort_adv(query, group_filters: dict):
    from sqlalchemy import asc, desc
    association_table = {
        "id": models.Advertisements.id,
        "title": models.Advertisements.title,
        "content": models.Advertisements.content,
        "date_of_publication": models.Advertisements.date_of_publication,
    }
    sort_table = {
        "asc": asc,
        "desc": desc
    }
    asc_or_desc = sort_table.get(group_filters.get("group_by"))
    db_column = association_table.get(group_filters.get("sort_by"))
    query = query.order_by(asc_or_desc(db_column))

    return query

def complaint_advertisement(complaint: adv_schemas.ComplaintIn, db: Session, current_user):
    if find_adv_for_id(db=db, id=complaint.advertisement_id) is None:
        raise HTTPException(
            status_code=403,
            detail="Advertisement not found"
                )
    find_complaint = db.query(models.Complaint).\
        filter(
            models.Complaint.user_id == current_user.id,
            models.Complaint.advertisement_id == complaint.advertisement_id,
                ).one_or_none()
    if find_complaint:
        raise HTTPException(
            status_code=403,
            detail="You have already left a complaint"
                )
    complaint = models.Complaint(
            advertisement_id=complaint.advertisement_id,
            user_id=current_user.id,
            message=complaint.message,
            type_of_complaint=complaint.type_of_complaint
        )
    try:
        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        return complaint
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Incorrectly filled fields"
                )


def get_complaint_interresting_adv(adv_id: int, db: Session):
    if find_adv_for_id(db=db, id=adv_id) is None:
        raise HTTPException(
            status_code=403,
            detail="Advertisement not found"
                )
    adv = db.query(models.Complaint).filter(models.Complaint.advertisement_id == adv_id).all()
    return adv