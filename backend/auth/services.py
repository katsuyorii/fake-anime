from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import UserModel
from .schemas import UserRegisterSchema
from .utils import hashing_password


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