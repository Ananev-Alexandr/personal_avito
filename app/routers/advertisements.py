from fastapi import APIRouter
from app.schemas import adv_schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db_connect import get_db
from app.security import services
from app.database import crud

router = APIRouter(tags=["Advertisements"])


@router.post("/advertisements/", response_model=adv_schemas.AdvDB)
async def create_advertisements(
    adv: adv_schemas.AdvIn,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.create_advertisement(db=db, adv=adv, user_id=current_user.id, current_user=current_user)


@router.post("/all_advertisements/")
async def all_advertisements(
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.get_all_adv(db=db, current_user=current_user)


@router.get("/advertisements/{id}/", response_model=adv_schemas.AdvDB)
async def info_about_adv(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.info_about_adv(id=id, db=db, current_user=current_user)


@router.delete("/advertisements/{id}/")
async def delete_advt(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    return crud.delete_adv(id=id, user_id=current_user.id, db=db, current_user=current_user)


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