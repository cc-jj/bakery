from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src import auth, crud
from src.dependencies import get_db


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


class LoginSchema(BaseModel):
    username: str
    password: str


@router.post("/token")
def login(schema: LoginSchema, db: Session = Depends(get_db)):
    db_user = crud.read_user(db, schema.username)
    if db_user is not None:
        if auth.verify_password(schema.password, db_user.hashed_password):
            token = auth.create_access_token(schema.username)
            return {"token": token}
    raise HTTPException(400, "Username or password is incorrect")
