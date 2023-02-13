import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker

from src import settings


def _create_engine():
    connect_args = None
    if "sqlite" in settings.SQLALCHEMY_DATABASE_URL:
        connect_args = {"check_same_thread": False}
    return sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args=connect_args)


engine = _create_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
