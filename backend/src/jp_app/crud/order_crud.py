from typing import List

from sqlalchemy import delete
from sqlalchemy.orm import Session
from schemas.order_schema import OrderCreate
from models.order_model import Order


def create_order(db: Session, order: OrderCreate) -> Order:
    db_order = Order(**order.__dict__)
    db.add(db_order)
    db.commit()

    return db_order


def get_all_orders(db: Session) -> List[Order]:
    orders = db.query(Order).all()

    return orders


def get_order_by_id(db: Session, order_id: int) -> Order:
    query = db.query(Order).filter(Order.id == order_id).first()

    return query


def delete_order(db: Session, order_id: int) -> None:
    query = (
        delete(Order)
        .where(Order.id == order_id)
        .execution_options(synchronize_session="fetch")
    )
    db.execute(query)
    db.commit()
