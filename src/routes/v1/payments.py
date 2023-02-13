from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from src import crud, schemas
from src.dependencies import get_db

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)


def _parse_date(value: str | None) -> date | None:
    if value is None:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


@router.post("", response_model=schemas.Order, status_code=201)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    if crud.read_order(db, payment.order_id) is None:
        raise HTTPException(404, f"Order {payment.order_id} does not exist")
    return crud.create_payment(db, payment)


@router.patch("/{payment_id}", response_model=schemas.Order)
def update_payment(payment_id: int, payment: schemas.PaymentEdit, db: Session = Depends(get_db)):
    if crud.read_order(db, payment.order_id) is None:
        raise HTTPException(404, f"Order {payment.order_id} does not exist")
    if crud.read_payment(db, payment_id) is None:
        raise HTTPException(4040, f"Payment {payment_id} does not exist")
    return crud.update_payment(db, payment_id, payment)


@router.get("", response_model=LimitOffsetPage[schemas.Payment])
def get_payments(
    inclusive_start_date: str | None = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    exclusive_end_date: str | None = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    db: Session = Depends(get_db),
):
    # TODO order by
    query = crud.read_payments(
        db,
        _parse_date(inclusive_start_date),
        _parse_date(exclusive_end_date),
    )
    return paginate(query)


@router.delete("/{payment_id}", response_model=schemas.Order)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    return crud.delete_payment(db, payment_id)
