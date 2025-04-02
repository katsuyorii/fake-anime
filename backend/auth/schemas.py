import re

from pydantic import BaseModel, EmailStr, field_validator

from fastapi import HTTPException


REGEX_PASSWORD = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")

class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator('password', mode='before')
    @classmethod
    def validate_password(cls, value):
        if not REGEX_PASSWORD.match(value):
            raise HTTPException(
                status_code=422,
                detail="Пароль должен содержать минимум 8 символов, хотя бы одну заглавную букву, одну строчную букву, одну цифру и один специальный символ (#?!@$%^&*-)."
            )
        return value