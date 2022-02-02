import json
from datetime import datetime, timezone

import freezegun
import pytest

from src import crud, models, schemas


def test_create_edit(client, auth_headers):
    client.headers.update(auth_headers)

    # create
    payload = {
        "name": "cj",
        "email": "cj@domain.com",
        "phone": "(330) 867-5309",
        "notes": "a note",
    }
    date_created = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_created):
        response = client.post("/api/v1/customers", json=payload)
    assert response.status_code == 201
    customer = response.json()
    assert customer == {
        **payload,
        "id": 1,
        "date_created": date_created.isoformat(),
        "date_modified": date_created.isoformat(),
    }

    # edit
    payload = {**payload, "notes": "a new note"}
    date_modified = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_modified):
        response = client.patch("/api/v1/customers/1", json=payload)
    assert response.status_code == 200
    customer = response.json()
    assert customer == {
        **payload,
        "id": 1,
        "date_created": date_created.isoformat(),
        "date_modified": date_modified.isoformat(),
    }


def test_get(client, auth_headers, customer_cj, customer_sarah, customer_sarah_2):

    client.headers.update(auth_headers)

    # get by id
    response = client.get(f'/api/v1/customers/{customer_cj["id"]}')
    assert response.status_code == 200
    assert response.json() == customer_cj

    # get all
    response = client.get("/api/v1/customers")
    assert response.status_code == 200
    assert response.json() == {
        "total": 3,
        "limit": 50,
        "offset": 0,
        "items": [customer_cj, customer_sarah, customer_sarah_2],
    }

    # get by name
    response = client.get("/api/v1/customers?name=sarah")
    assert response.status_code == 200
    assert response.json() == {
        "total": 2,
        "limit": 50,
        "offset": 0,
        "items": [customer_sarah, customer_sarah_2],
    }

    # get by email
    for customer in (customer_cj, customer_sarah, customer_sarah_2):
        response = client.get(f'/api/v1/customers?email={customer["email"]}')
        assert response.status_code == 200
        assert response.json() == {
            "total": 1,
            "limit": 50,
            "offset": 0,
            "items": [customer],
        }

    # get by phone
    for customer in (customer_cj, customer_sarah, customer_sarah_2):
        response = client.get(f'/api/v1/customers?phone={customer["phone"]}')
        assert response.status_code == 200
        assert response.json() == {
            "total": 1,
            "limit": 50,
            "offset": 0,
            "items": [customer],
        }

    # get by name and phone and email
    for customer in (customer_cj, customer_sarah, customer_sarah_2):
        response = client.get(
            f'/api/v1/customers?name={customer["name"]}&email={customer["email"]}&phone={customer["phone"]}',
        )
        assert response.status_code == 200
        assert response.json() == {
            "total": 1,
            "limit": 50,
            "offset": 0,
            "items": [customer],
        }


def test_unauthorized(client, invalid_auth_headers):
    client.headers.update(invalid_auth_headers)
    assert client.post("/api/v1/customers").status_code == 403
    assert client.patch("/api/v1/customers/1").status_code == 403
    assert client.get("/api/v1/customers/1").status_code == 403
    assert client.get("/api/v1/customers").status_code == 403


def serialize_customer(customer: models.Customer):
    return json.loads(schemas.Customer.from_orm(customer).json())


@pytest.fixture
def customer_cj(db):
    return serialize_customer(
        crud.create_customer(
            db,
            schemas.CustomerCreate(
                name="cj", email="cj@domain.com", phone="(330) 867-5309"
            ),
        )
    )


@pytest.fixture
def customer_sarah(db):
    return serialize_customer(
        crud.create_customer(
            db,
            schemas.CustomerCreate(
                name="sarah", email="sarah@domain.com", phone="(714) 867-5309"
            ),
        )
    )


@pytest.fixture
def customer_sarah_2(db):
    return serialize_customer(
        crud.create_customer(
            db,
            schemas.CustomerCreate(
                name="sarah", email="sarah2@domain.com", phone="(216) 867-5309"
            ),
        )
    )
