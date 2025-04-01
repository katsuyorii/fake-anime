from sqlalchemy import String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime, date
from enum import Enum

from src.database import BaseModel


class UserRole(str, Enum):
    user = 'user'
    admin = 'admin'

class UserModel(BaseModel):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(default=UserRole.user)
    first_name: Mapped[str] = mapped_column(String(256), nullable=True)
    last_name: Mapped[str] = mapped_column(String(256), nullable=True)
    date_of_birth: Mapped[date] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(server_default=text('False'))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
