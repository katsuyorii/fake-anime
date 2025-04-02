from fastapi import HTTPException, Response, Request

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from redis.asyncio import Redis

from datetime import timedelta

from src.config import settings
from users.models import UserModel
from .schemas import TokenResponseSchema, UserRegisterSchema, UserLoginSchema
from .utils import hashing_password, verify_password, create_access_token, create_refresh_token,  verify_refresh_token, add_token_to_blacklist, is_token_to_blacklist
from .exceptions import INVALID_CREDENTIALS_ERROR


async def registration(user_data: UserRegisterSchema, db: AsyncSession):
    result = await db.execute(select(UserModel).where(UserModel.email == user_data.email))
    existing_user = result.scalars().one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail='Пользователь с таким адресом электронной почты уже зарегестрирован в системе!'
        )

    user_data_dict = user_data.model_dump()
    user_data_dict['password'] = await hashing_password(user_data.password)

    user = UserModel(**user_data_dict)
    db.add(user)
    await db.flush()
    await db.commit()

async def login(user: UserLoginSchema, response: Response, db: AsyncSession) -> TokenResponseSchema:
    result = await db.execute(select(UserModel).where(UserModel.email == user.email))
    existing_user = result.scalars().one_or_none()

    if not existing_user:
        raise INVALID_CREDENTIALS_ERROR
    
    if not await verify_password(user.password, existing_user.password):
        raise INVALID_CREDENTIALS_ERROR
    
    access_token = await create_access_token({
        'sub': str(existing_user.id),
    })

    refresh_token = await create_refresh_token({
        'sub': str(existing_user.id),
    })

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=True,
        max_age=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        samesite='Strict',
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        max_age=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        samesite='Strict',
    )

    return TokenResponseSchema(access_token=access_token)

async def logout(request: Request, response: Response, redis: Redis):
    refresh_token = request.cookies.get('refresh_token')
    await add_token_to_blacklist(refresh_token, redis)

    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

async def refresh(request: Request, response: Response, redis: Redis) -> TokenResponseSchema:
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token отсутствует!"
        )
    
    if await is_token_to_blacklist(refresh_token, redis):
        raise HTTPException(
            status_code=401,
            detail='Refresh токен заблокирован!'
        )
    
    payload = await verify_refresh_token(refresh_token)

    new_access_token = await create_access_token(payload)

    response.set_cookie(
        key='access_token',
        value=new_access_token,
        secure=True,
        httponly=True,
        max_age=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        samesite='Strict',
    )

    return TokenResponseSchema(access_token=new_access_token)