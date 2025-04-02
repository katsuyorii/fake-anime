import jwt
import bcrypt

from fastapi import HTTPException

from redis.asyncio import Redis

from datetime import datetime, timedelta, timezone

from time import time

from src.config import settings


async def hashing_password(password: str) -> str:
    password_bytes = password.encode()
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password_bytes, salt).decode()

async def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

async def create_access_token(payload: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = payload.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({'exp': expire})

    access_token = jwt.encode(payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return access_token

async def create_refresh_token(payload: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = payload.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({'exp': expire})

    refresh_token = jwt.encode(payload=to_encode, key=settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)

    return refresh_token

async def verify_refresh_token(refresh_token: str) -> dict:
    try:
        payload = jwt.decode(jwt=refresh_token, key=settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Refresh токен истёк. Пожалуйста, войдите снова.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Недействительный refresh токен. Проверьте правильность данных.",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def add_token_to_blacklist(refresh_token: str, redis: Redis):
    payload = await verify_refresh_token(refresh_token)
    exp = payload.get('exp')

    expires_in = exp - int(time())
    await redis.setex(refresh_token, expires_in, "blacklisted")