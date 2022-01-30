from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from src import auth, crud, database, models


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


_http_bearer = HTTPBearer()


def get_authorized_user(
    creds: HTTPAuthorizationCredentials = Depends(_http_bearer),
    db: Session = Depends(get_db),
) -> models.User:
    try:
        username = auth.decode_username(creds.credentials)
    except JWTError:
        raise HTTPException(403, "Credentials invalid or expired")

    if username is not None:
        user = crud.read_user(db, username)
        if user is not None:
            return user

    raise HTTPException(403, "Could not validate credentials")
