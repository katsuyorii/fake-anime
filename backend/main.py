from fastapi import FastAPI

from auth.routers import auth_router
from users.routers import users_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)