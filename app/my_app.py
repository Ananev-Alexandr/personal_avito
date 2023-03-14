from fastapi import FastAPI

from app.routers.users import router as user_router
from app.routers.advertisements import router as adv_router

app = FastAPI()


app.include_router(user_router)
app.include_router(adv_router)