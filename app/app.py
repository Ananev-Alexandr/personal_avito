from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.application_objects.users.router import router as user_router
from app.application_objects.advertisements.router import router as adv_router
from app.application_objects.token.router import router as token_router


app = FastAPI()


app.include_router(user_router)
app.include_router(adv_router)
app.include_router(token_router)

add_pagination(app)