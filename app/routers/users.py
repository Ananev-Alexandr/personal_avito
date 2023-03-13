from fastapi import APIRouter

router = APIRouter(tags=["users"])


@router.get("/")
async def hello() -> dict:
    return {"Hello": "World"}