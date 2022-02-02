from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from src import crud, schemas
from src.dependencies import get_db

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/items", response_model=schemas.Order, status_code=201)
def create_order_item(order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    return crud.create_order_item(db, order_item)


@router.patch("/items/{order_item_id}", response_model=schemas.Order)
def update_order_item(
    order_item_id: int, order_item: schemas.OrderItemEdit, db: Session = Depends(get_db)
):
    return crud.update_order_item(db, order_item_id, order_item)


@router.delete("/items/{order_item_id}", response_model=schemas.Order)
def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
    return crud.delete_order_item(db, order_item_id)


@router.post("", response_model=schemas.Order, status_code=201)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


@router.get("/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return crud.read_order(db, order_id)


@router.get("", response_model=LimitOffsetPage[schemas.Order])
def get_orders(completed: bool, db: Session = Depends(get_db)):
    # TODO order by
    query = crud.read_orders(db, completed)
    return paginate(query)


@router.patch("/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderEdit, db: Session = Depends(get_db)):
    return crud.update_order(db, order_id, order)


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    success = crud.delete_order(db, order_id)
    content = jsonable_encoder({"success": success})
    return JSONResponse(content)
