from typing import List, Union

from sqlalchemy import delete, update
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserCreate, UserDTO
from ..models.user_model import User
from ..password_hashing import hashing_password


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        telefone=user.telefone,
        address=user.address,
        password=hashing_password.Hasher.get_hash_password(user.password),
    )
    db.add(db_user)
    db.commit()

    return db_user


def get_all_users(db: Session) -> List[UserDTO]:
    users = db.query(User).all()

    return users


def get_user_by_id(db: Session, user_id: int) -> User:
    query = db.query(User).filter(User.id == user_id).first()

    return query


def check_if_user_exists(db: Session, user: Union[UserDTO, UserCreate]) -> User:
    query = (
        db.query(User)
        .filter(
            User.first_name == user.first_name
            and User.last_name == user.last_name
            and User.email == user.email
        )
        .first()
    )

    return query


def update_single_user(db: Session, user: User, user_modified: UserCreate) -> None:
    values = {k: v for k, v in user_modified.__dict__.items() if v is not None}

    query = update(User).where(User.id == user.id).values(**values)

    db.execute(query)
    db.commit()


def delete_user(db: Session, user_id: int) -> None:
    query = (
        delete(User)
        .where(User.id == user_id)
        .execution_options(synchronize_session="fetch")
    )
    db.execute(query)
    db.commit()
