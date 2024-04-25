from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime

from sqlalchemy.sql import func
from backend.src.jp_app.database import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(length=120))
    last_name = Column(String(length=120))
    email = Column(String(length=120))
    telefone = Column(String(length=120))
    address = Column(String(length=120))
    password = Column(String(length=128))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    # Products that the user sells
    products = relationship("Product", back_populates="user",  uselist=True)
    # Order that the user places to buy
    my_orders = relationship("Order", back_populates="user",  uselist=True)