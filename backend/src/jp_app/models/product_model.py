from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime

from sqlalchemy.sql import func
from database.config import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    availability = Column(Boolean)
    name = Column(String)
    details = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    user_id = Column(Integer, ForeignKey("users.id", name="fk_user"))

    user = relationship("User", back_populates="products")
