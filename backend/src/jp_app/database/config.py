from os import getenv


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


SQLALCHEMY_DATABASE_URL = getenv('DATABASE_URL', 'sqlite:///./sqlite.db')


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

BaseModel = declarative_base(name="Model")


def init_db() -> None:
    BaseModel.metadata.create_all(bind=engine)


# Dependency
def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()