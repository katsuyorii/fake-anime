import bcrypt

async def hashing_password(password: str) -> str:
    password_bytes = password.encode()
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password_bytes, salt).decode()