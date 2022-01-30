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


@router.post("/", response_model=schemas.Customer, status_code=201)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)


@router.patch("/", response_model=schemas.Customer)
def update_customer(customer: schemas.CustomerEdit, db: Session = Depends(get_db)):
    return crud.update_customer(db, customer)


@router.get("/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.read_customer(db, customer_id)
    if customer is None:
        raise HTTPException(404, "Customer not found")
    return customer


@router.get("/", response_model=LimitOffsetPage[schemas.Customer])
def get_customers(
    name: str = None,
    email: str = None,
    phone: str = None,
    db: Session = Depends(get_db),
):
    # TODO order by
    query = crud.read_customers(db, name, email, phone)
    return paginate(query)
