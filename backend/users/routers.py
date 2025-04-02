from fastapi import APIRouter, Depends

from .models import UserModel
from .schemas import UserResponseSchema
from .dependencies import get_current_user

users_router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

@users_router.get('/me', response_model=UserResponseSchema)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user