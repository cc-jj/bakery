from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from src import crud, schemas
from src.dependencies import get_db

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.post("", response_model=schemas.Customer, status_code=201)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)


@router.patch("/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_id: int, customer: schemas.CustomerEdit, db: Session = Depends(get_db)
):
    return crud.update_customer(db, customer_id, customer)


@router.get("/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.read_customer(db, customer_id)
    if customer is None:
        raise HTTPException(404, f"Customer {customer_id} not found")
    return customer


@router.get("", response_model=LimitOffsetPage[schemas.Customer])
def get_customers(
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    orderBy: str = "name",
    descending: str | None = None,
    db: Session = Depends(get_db),
):
    if orderBy and orderBy not in {"name", "email", "phone"}:
        raise HTTPException(400, "orderby must be one of name, email, phone")
    query = crud.read_customers(db, name, email, phone, orderBy, descending is not None)
    return paginate(query)
