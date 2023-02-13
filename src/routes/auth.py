from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src import auth, crud, schemas
from src.dependencies import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


class LoginSchema(BaseModel):
    username: str
    password: str


@router.post("/login", response_model=schemas.User)
def login(schema: LoginSchema, response: Response, db: Session = Depends(get_db)):
    db_user = crud.read_user(db, schema.username)
    if db_user is not None:
        if auth.verify_password(schema.password, str(db_user.hashed_password)):
            auth.set_cookie(response, str(db_user.name))
            return schemas.User(id=db_user.id, name=db_user.name)
    raise HTTPException(400, "Username or password is incorrect")


@router.get("/logout")
def logout(response: Response):
    auth.remove_cookie(response)
    response.status_code = 204
    return response
