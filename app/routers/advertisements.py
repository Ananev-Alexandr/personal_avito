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
    security=Depends(services.get_current_user)
        ):
    return crud.create_advertisement(db=db, adv=adv, user_id=security.id)