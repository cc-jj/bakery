from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from src import crud, schemas
from src.dependencies import get_db

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)


@router.post("", response_model=schemas.Order, status_code=201)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    return crud.create_payment(db, payment)


@router.patch("/{payment_id}", response_model=schemas.Order)
def update_payment(payment_id: int, payment: schemas.PaymentEdit, db: Session = Depends(get_db)):
    return crud.update_payment(db, payment_id, payment)


@router.get("", response_model=LimitOffsetPage[schemas.Payment])
def get_payments(
    inclusive_start_date: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    exclusive_end_date: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    db: Session = Depends(get_db),
):
    # TODO order by
    if inclusive_start_date is not None:
        inclusive_start_date = datetime.strptime(inclusive_start_date, "%Y-%m-%d")
    if exclusive_end_date is not None:
        exclusive_end_date = datetime.strptime(exclusive_end_date, "%Y-%m-%d")
    query = crud.read_payments(db, inclusive_start_date, exclusive_end_date)
    return paginate(query)


@router.delete("/{payment_id}", response_model=schemas.Order)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    return crud.delete_payment(db, payment_id)
