from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from src import auth, crud, database, models


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_authorized_user(
    request: Request,
    db: Session = Depends(get_db),
) -> models.User:
    session = auth.verify_cookie(request)
    user = crud.read_user(db, session["username"])
    if user is None:
        raise HTTPException(HTTP_403_FORBIDDEN, "Could not validate credentials")
    return user
