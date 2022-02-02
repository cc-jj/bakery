from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from src import crud, schemas
from src.dependencies import get_db

router = APIRouter(
    prefix="/menu",
    tags=["menu"],
)


@router.post("/categories", response_model=schemas.MenuCategory, status_code=201)
def create_menu_category(
    category: schemas.MenuCategoryCreate, db: Session = Depends(get_db)
):
    return crud.create_menu_category(db, category)


@router.patch("/categories/{category_id}", response_model=schemas.MenuCategory)
def update_menu_category(
    category_id: int,
    menu_category: schemas.MenuCategoryEdit,
    db: Session = Depends(get_db),
):
    return crud.update_menu_category(db, category_id, menu_category)


@router.get("/categories/{category_id}", response_model=schemas.MenuCategory)
def get_menu_category(category_id: int, db: Session = Depends(get_db)):
    menu_category = crud.read_menu_category(db, category_id)
    if menu_category is None:
        raise HTTPException(404, "Customer not found")
    return menu_category


@router.get("/categories", response_model=LimitOffsetPage[schemas.MenuCategory])
def get_menu_categories(db: Session = Depends(get_db)):
    # TODO order by
    query = crud.read_menu_categories(db)
    return paginate(query)


@router.post("", response_model=schemas.MenuItem, status_code=201)
def create_menu_item(category: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    return crud.create_menu_item(db, category)


@router.get("", response_model=LimitOffsetPage[schemas.MenuItem])
def get_menu(category_id: int = None, db: Session = Depends(get_db)):
    # TODO order by
    query = crud.read_menu_items(db, category_id)
    return paginate(query)


@router.patch("/{menu_item_id}", response_model=schemas.MenuItem)
def update_menu_item(
    menu_item_id: int, menu_item: schemas.MenuItemEdit, db: Session = Depends(get_db)
):
    return crud.update_menu_item(db, menu_item_id, menu_item)


@router.get("/{menu_item_id}", response_model=schemas.MenuItem)
def get_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    menu_item = crud.read_menu_item(db, menu_item_id)
    if menu_item is None:
        raise HTTPException(404, "Customer not found")
    return menu_item
