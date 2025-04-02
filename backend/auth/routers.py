from fastapi import APIRouter, Depends, Response, Request

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.redis import get_redis
from .schemas import TokenResponseSchema, UserRegisterSchema, UserLoginSchema
from .services import registration, login, logout


auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@auth_router.post('/register', status_code=201)
async def registration_user(user_data: UserRegisterSchema, db: AsyncSession = Depends(get_session)):
    await registration(user_data, db)

    return {'message': 'Пользователь успешно зарегистрирован!'}

@auth_router.post('/login', response_model=TokenResponseSchema)
async def login_user(user: UserLoginSchema, response: Response, db: AsyncSession = Depends(get_session)):
    return await login(user, response, db)

@auth_router.post('/logout')
async def logout_user(request: Request, response: Response, redis = Depends(get_redis)):
    await logout(request, response, redis)

    return {"message": "Вы успещно вышли из системы!"}