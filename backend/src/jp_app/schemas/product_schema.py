from typing import Optional

from datetime import datetime
from pydantic import BaseModel, constr


class ProductCreate(BaseModel):
    id: Optional[int] = None
    name: constr(max_length=120)
    price: float
    availability: bool = False
    details: constr(max_length=120)
    user_id: int

    time_created: datetime = datetime.now()
    time_updated: datetime = datetime.now()


class ProductDTO(BaseModel):
    id: Optional[int] = None
    price: float
    name: constr(max_length=120)
    availability: bool = False

    class Config:
        orm_mode = True