from fastapi import APIRouter
from app.schemas import adv_schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db_connect import get_db
from app.security import services
from app.application_objects.advertisements import crud

router = APIRouter(tags=["Advertisements"])


@router.post("/advertisements/", response_model=adv_schemas.AdvDB)
async def create_advertisements(
    adv: adv_schemas.AdvIn,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.create_advertisement(db=db, adv=adv, user_id=current_user.id)


@router.post("/all_advertisements/")
async def all_advertisements(
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.get_all_adv(db=db)

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


@router.get("/advertisements/{id}")
async def feedback_interesting_adv(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.feedback_interesting_adv(id=id, db=db)


@router.get("/advertisements/{id}/")
async def info_about_adv(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.info_about_adv(id=id, db=db)


@router.delete("/advertisements/{id}/")
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

