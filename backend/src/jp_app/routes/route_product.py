from typing import List

from fastapi import Depends, HTTPException
from fastapi import Response, APIRouter, status
from sqlalchemy.orm import Session

from crud import product_crud
from database.config import get_db
from schemas.product_schema import ProductCreate, ProductDTO

router = APIRouter()
feature_flag = "PRODUCT_ROUTE"


@router.post("/products", tags=["product"])
async def create_product(
    response: Response, product: ProductCreate, db: Session = Depends(get_db)
):
    db_product = product_crud.check_if_product_exists(db=db, product=product)

    if db_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Product already registered"
        )
    new_product = product_crud.create_product(db=db, product=product)

    if new_product:
        response.status_code = status.HTTP_201_CREATED
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return new_product


@router.get("/products", response_model=List[ProductDTO], tags=["product"])
async def get_products(db: Session = Depends(get_db)):

    return product_crud.get_all_products(db=db)


@router.get("/products/{product_id}", response_model=ProductDTO, tags=["product"])
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = product_crud.get_product_by_id(db=db, product_id=product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    else:

        return product


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["product"])
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_crud.delete_product(db=db, product_id=product_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
