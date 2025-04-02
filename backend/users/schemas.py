from pydantic import BaseModel, ConfigDict, EmailStr

from datetime import datetime, date

from .models import UserRole


class BaseORMSchema(BaseModel):
    ''' Base schema class for convert to json (ORM) '''
    model_config = ConfigDict(from_attributes=True)

class UserResponseSchema(BaseORMSchema):
    id: int
    email: EmailStr
    role: UserRole
    first_name: str | None
    last_name: str | None
    date_of_birth: date | None
    is_active: bool
    created_at: datetime