from fastapi import APIRouter, Depends, HTTPException, Response
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


@router.post("/login")
def login(schema: LoginSchema, response: Response, db: Session = Depends(get_db)):
    db_user = crud.read_user(db, schema.username)
    if db_user is not None:
        if auth.verify_password(schema.password, db_user.hashed_password):
            auth.set_cookie(response, db_user.name)
            response.status_code = 200
            return response
    raise HTTPException(400, "Username or password is incorrect")


@router.get("/logout")
def logout(response: Response):
    auth.remove_cookie(response)
    response.status_code = 200
    return response
