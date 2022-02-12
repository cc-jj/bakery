from fastapi import APIRouter, Depends

from src import models, schemas
from src.dependencies import get_authorized_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=schemas.User)
def me(user: models.User = Depends(get_authorized_user)):
    return schemas.User(id=user.id, name=user.name)
