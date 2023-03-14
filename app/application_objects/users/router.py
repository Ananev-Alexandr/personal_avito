from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.database.db_connect import get_db
from app.application_objects.users import crud
from app.schemas import user_schemas
from app.security import services


router = APIRouter(tags=["users"])


@router.post("/users/", response_model=user_schemas.UserOut)
async def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@router.put("/ban/{id}")
async def ban(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_admin)
    ):
    return crud.ban(db=db, id=id)


@router.put("/give_root_admin/{id}")
async def give_root_admin(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(services.get_current_admin)
    ):
    return crud.give_root_admin(db=db, id=id)

      

   

