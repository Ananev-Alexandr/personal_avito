from fastapi import APIRouter
from app.schemas import adv_schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db_connect import get_db
from app.security import services
from app.application_objects.advertisements import crud
from fastapi_pagination import paginate, Page


router = APIRouter(tags=["Advertisements"])


@router.post("/create_advertisements/", response_model=adv_schemas.AdvDB)
async def create_advertisements(
    adv: adv_schemas.AdvIn,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.create_advertisement(db=db, adv=adv, user_id=current_user.id)


@router.post("/all_advertisements/", response_model=Page[adv_schemas.FilterAdv])
async def all_advertisements(
    filter_and_sort: adv_schemas.FilterAndSortAdv,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return paginate(crud.get_all_adv(filter_and_sort=filter_and_sort, db=db))

@router.post("/feedback/")
async def post_a_feedback(
    fb: adv_schemas.FeedbackIn,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.post_a_feedback(
        feedback=fb,
        user_id=current_user.id,
        db=db
        )


@router.post("/finde_feedback/{adv_id}/")
async def finde_feedback(
    adv_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_admin)
        ):
    return crud.finde_feedback(adv_id=adv_id,db=db)


@router.post("/complaint_advertisement/{adv_id}/")
async def complaint_advertisement(
    complaint: adv_schemas.ComplaintIn,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.complaint_advertisement(complaint=complaint,db=db,current_user=current_user)


@router.get("/feedback_interesting_adv/{id}")
async def feedback_interesting_adv(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.feedback_interesting_adv(id=id, db=db)


@router.get("/info_about_adv/{id}/")
async def info_about_adv(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.info_about_adv(id=id, db=db)

@router.get("/complaint/{adv_id}/")
async def get_complaint_interresting_adv(
    adv_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_admin)
        ):
    return crud.get_complaint_interresting_adv(adv_id=adv_id, db=db)
    

@router.put("/сhanging_the_group_adv/{id}/")
async def сhanging_the_group_adv(
    id: int,
    new_group: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_admin)
        ):
    return crud.сhanging_the_group_adv(id=id, db=db, new_group=new_group)


@router.delete("/delete_advertisements/{id}/")
async def delete_advt(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.delete_adv(id=id, user_id=current_user.id, db=db)


@router.delete("/delete_feedback_advertisements/{feedback_id}/")
async def delete_feedback_advt_by_admin(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_admin)
        ):
    return crud.delete_feedback_advt_by_admin(feedback_id=feedback_id, db=db)

