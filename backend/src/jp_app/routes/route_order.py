from typing import List

from fastapi import Depends, HTTPException
from fastapi import Response, APIRouter, status
from sqlalchemy.orm import Session

from crud import order_crud
from database.config import get_db
from schemas.order_schema import OrderCreate, OrderDTO

router = APIRouter()
feature_flag = "ORDER_ROUTE"


@router.post("/orders", response_model=OrderDTO, tags=["order"])
async def create_order(order: OrderCreate, db: Session = Depends(get_db)
):
    return order_crud.create_order(db=db, order=order)


@router.get("/orders", response_model=List[OrderDTO], tags=["order"])
async def get_orders(db: Session = Depends(get_db)):

    return order_crud.get_all_orders(db=db)


@router.get("/orders/{order_id}", response_model=OrderDTO, tags=["order"])
async def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = order_crud.get_order_by_id(db=db, order_id=order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    else:

        return order


@router.delete("/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["order"])
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order_crud.delete_order(db=db, order_id=order_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
