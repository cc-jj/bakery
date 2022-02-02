import json
from typing import Type

import pydantic
import pytest
from fastapi.testclient import TestClient

from src import auth, crud, database, models, schemas
from src.database import Base, SessionLocal
from src.dependencies import get_db
from src.main import app


@pytest.fixture(scope="session")
def db_engine():
    database.Base.metadata.create_all(bind=database.engine)
    return database.engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual Session to the connection
    db = SessionLocal(bind=connection)

    yield db

    db.rollback()
    connection.close()


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as client:
        yield client


def serialize_model(model: Base, schema_cls: Type[pydantic.BaseModel]):
    return json.loads(schema_cls.from_orm(model).json())


@pytest.fixture
def user(db):
    db_user = models.User(name="cj", hashed_password=auth.pwd_context.hash("hunter123"))
    db.add(db_user)
    db.commit()
    return db_user


@pytest.fixture
def auth_headers(db, user):
    token = auth.create_access_token("cj")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def invalid_auth_headers():
    token = auth.create_access_token("not-a-user")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def customer(db):
    model = crud.create_customer(db, schemas.CustomerCreate(name="cj"))
    return serialize_model(model, schemas.Customer)


@pytest.fixture
def campaign(db):
    model = crud.create_campaign(
        db, schemas.CampaignCreate(name="Open Porch", description="Outdoor invitation")
    )
    return serialize_model(model, schemas.Campaign)


@pytest.fixture
def menu_category(db):
    model = crud.create_menu_category(
        db, schemas.MenuCategoryCreate(name="Cocoa Bombs")
    )
    return serialize_model(model, schemas.MenuCategory)


@pytest.fixture
def menu_item(db, menu_category):
    model = crud.create_menu_item(
        db,
        schemas.MenuItemCreate(
            name="Chocolate cocoa bomb",
            category_id=menu_category["id"],
            price=5.0,
            price_units="each",
        ),
    )
    return serialize_model(model, schemas.MenuItem)


@pytest.fixture
def order(db, customer, menu_item):
    model = crud.create_order(
        db,
        schemas.OrderCreate(
            customer_id=customer["id"],
            order_items=[
                schemas.OrderItemCreateNewOrder(
                    menu_item_id=menu_item["id"],
                    quantity=4,
                    menu_price=4 * menu_item["price"],
                    charged_price=4 * menu_item["price"],
                )
            ],
        ),
    )
    return serialize_model(model, schemas.Order)
