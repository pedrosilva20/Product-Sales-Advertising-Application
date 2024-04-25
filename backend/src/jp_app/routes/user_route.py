from typing import List, Optional

from fastapi import Depends, HTTPException
from fastapi import Response, APIRouter, status
from sqlalchemy.orm import Session

from crud import user_crud
from backend.src.jp_app.database import get_db
from ..schemas.user_schema import UserCreate, UserDTO

router = APIRouter()
feature_flag = "USER_ROUTE"


@router.post("/users", tags=["user"])
async def create_user(
    response: Response, user: UserCreate, db: Session = Depends(get_db)
):
    db_user = user_crud.check_if_user_exists(db=db, user=user)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already registered"
        )
    new_user = user_crud.create_user(db=db, user=user)

    if new_user:
        response.status_code = status.HTTP_201_CREATED
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return new_user


@router.get("/users",response_model=List[UserDTO], tags=["user"])
async def get_users(db: Session = Depends(get_db)):

    return user_crud.get_all_users(db=db)


@router.get("/users/{user_id}", response_model=UserDTO, tags=["user"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    else:
        return user


@router.put("/users/{user_id}", tags=["user"])
async def update_user(
    user_id: int,
    user: Optional[UserCreate] = None,
    db: Session = Depends(get_db),
):
    user_to_be_modified = user_crud.get_user_by_id(db=db, user_id=user_id)

    if not user_to_be_modified:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user:
        user_crud.update_single_user(
            db=db, user=user_to_be_modified, user_modified=user
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["user"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_crud.delete_user(db=db, user_id=user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
