from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from sqlalchemy.sql import func
from database.config import BaseModel


class Order(BaseModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quantity = Column(Integer)
    delivery_address = Column(String(length=120))
    comments = Column(String(length=120))

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    # An order is related to a product, has two relationships, user_id and product_id
    user_id = Column(Integer, ForeignKey("users.id", name="fk_user_order"))
    product_id = Column(Integer, ForeignKey("products.id", name="fk_product_order"))

    product = relationship("Product")
    user = relationship("User", back_populates="my_orders")


