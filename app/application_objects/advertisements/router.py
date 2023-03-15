from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.application_objects.advertisements import crud
from app.database.db_connect import get_db
from app.schemas import adv_schemas
from app.security import services

router = APIRouter(tags=["Advertisements"])


@router.post("/create_advertisements/", response_model=adv_schemas.AdvDB)
async def create_advertisements(
    adv: adv_schemas.AdvIn,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    """Creating advertisements"""
    return await crud.create_advertisement(
        db=db,
        adv=adv,
        user_id=current_user.id
            )


@router.post(
    "/all_advertisements/",
    response_model=Page[adv_schemas.FilterAdv]
        )
async def all_advertisements(
    filter_and_sort: adv_schemas.FilterAndSortAdv,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    """Ability to receive all advertisements"""
    return paginate(crud.get_all_adv(filter_and_sort=filter_and_sort, db=db))


@router.post("/feedback/")
def post_a_feedback(
    fb: adv_schemas.FeedbackIn,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    """Sending feedback to the ad"""
    return crud.post_a_feedback(
        feedback=fb,
        user_id=current_user.id,
        db=db
        )


@router.get("/finde_feedback/{adv_id}/", response_model=Page[adv_schemas.FindFB])
async def finde_feedback(
    adv_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_admin)
        ):
    """Finding an ad of interest"""
    return paginate(crud.finde_feedback(adv_id=adv_id, db=db))


@router.post("/complaint_advertisement/{adv_id}/")
async def complaint_advertisement(
    complaint: adv_schemas.ComplaintIn,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    """Send a complaint about the advertisement"""
    return await crud.complaint_advertisement(
        complaint=complaint,
        db=db,
        current_user=current_user
            )


@router.get("/feedback_interesting_adv/{id}")
async def feedback_interesting_adv(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    """The user leaves feedback on a particular advertisement"""
    return await crud.feedback_interesting_adv(id=id, db=db)


@router.get("/info_about_adv/{id}/")
async def info_about_adv(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    """Getting information on the advertisements"""
    return await crud.info_about_adv(id=id, db=db)


@router.get("/complaint/{adv_id}/", response_model=Page[adv_schemas.ComplaintOut])
async def get_complaint_interresting_adv(
    adv_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_admin)
        ):
    """Getting a list of complaints left on the advertisements of interest"""
    return paginate(crud.get_complaint_interresting_adv(adv_id=adv_id, db=db))


@router.put("/сhanging_the_group_adv/{id}/")
async def сhanging_the_group_adv(
    id: int,
    new_group: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_admin)
        ):
    """The administrator can change the group
    in the advertisement of interest"""
    return await crud.сhanging_the_group_adv(id=id, db=db, new_group=new_group)


@router.delete("/delete_advertisements/{id}/")
async def delete_advt(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_user)
        ):
    """The user who created the ad can delete it"""
    return await crud.delete_adv(id=id, user_id=current_user.id, db=db)


@router.delete("/delete_feedback_advertisements/{feedback_id}/")
async def delete_feedback_advt_by_admin(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_admin)
        ):
    """The administrator can delete the review
    of the advertisement of interest"""
    return await crud.delete_feedback_advt_by_admin(
        feedback_id=feedback_id,
        db=db
            )
