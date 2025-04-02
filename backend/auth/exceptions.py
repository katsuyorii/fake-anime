from fastapi import HTTPException


INVALID_CREDENTIALS_ERROR = HTTPException(
    status_code=409,
    detail='Неверный адрес электронный почты или пароль!'
)