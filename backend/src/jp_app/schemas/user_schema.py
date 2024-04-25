from typing import Optional

from datetime import datetime
from pydantic import BaseModel, constr, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    first_name: constr(max_length=120)
    last_name: constr(max_length=120)
    telefone: constr(max_length=120)
    address: constr(max_length=120)


class UserCreate(UserBase):
    password: constr(max_length=64)


class UserDTO(UserBase):
    id: Optional[int]
    time_created: datetime = datetime.now()
    time_updated: datetime = datetime.now()

    class Config:
        orm_mode = True
