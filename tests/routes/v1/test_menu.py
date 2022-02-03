from datetime import datetime, timezone

import freezegun


def test_categories(client):

    # create
    payload = {
        "name": "Cocoa Bomb",
    }
    date_created = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_created):
        response = client.post("/api/v1/menu/categories", json=payload)
    assert response.status_code == 201
    category = response.json()
    assert category == {
        **payload,
        "id": 1,
        "date_created": date_created.isoformat(),
        "date_modified": date_created.isoformat(),
    }

    # edit
    payload = {**payload, "name": "Cocoa Bombs"}
    date_modified = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_modified):
        response = client.patch("/api/v1/menu/categories/1", json=payload)
    assert response.status_code == 200
    category = response.json()
    assert category == {
        **payload,
        "id": 1,
        "date_created": date_created.isoformat(),
        "date_modified": date_modified.isoformat(),
    }

    # get one
    response = client.get("/api/v1/menu/categories/1")
    assert response.status_code == 200
    assert response.json() == category

    # get many
    response = client.get("/api/v1/menu/categories?offset=0&limit=10")
    assert response.status_code == 200
    assert response.json() == {
        "items": [category],
        "limit": 10,
        "offset": 0,
        "total": 1,
    }


def test_create_category_unique_constraint(client, menu_category):

    payload = {"name": menu_category["name"]}
    response = client.post("/api/v1/menu/categories", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "A menu category already exists with that name"}


def test_edit_category_unique_constraint(client, menu_category):

    category_2 = {"name": "foo"}
    response = client.post("/api/v1/menu/categories", json=category_2)
    assert response.status_code == 201

    payload = {"name": "foo"}
    response = client.patch(f'/api/v1/menu/categories/{menu_category["id"]}', json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "A menu category already exists with that name"}


def test_menu_items(client, menu_category):

    # create
    payload = {
        "name": "Chocolate Cocoa Bomb",
        "category_id": menu_category["id"],
        "description": "Chocolate spherical cocoa bomb",
        "price": 5.0,
        "price_units": "each",
    }
    date_created = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_created):
        response = client.post("/api/v1/menu", json=payload)
    assert response.status_code == 201
    menu_item = response.json()
    assert menu_item == {
        **payload,
        "id": 1,
        "category": menu_category,
        "date_created": date_created.isoformat(),
        "date_modified": date_created.isoformat(),
    }

    # edit
    payload = {**payload, "price": 6.0}
    date_modified = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_modified):
        response = client.patch("/api/v1/menu/1", json=payload)
    assert response.status_code == 200
    menu_item = response.json()
    assert menu_item == {
        **payload,
        "id": 1,
        "category": menu_category,
        "date_created": date_created.isoformat(),
        "date_modified": date_modified.isoformat(),
    }

    # get one
    response = client.get("/api/v1/menu/1")
    assert response.status_code == 200
    assert response.json() == menu_item

    # get many
    response = client.get("/api/v1/menu?offset=0&limit=10")
    assert response.status_code == 200
    assert response.json() == {
        "items": [menu_item],
        "limit": 10,
        "offset": 0,
        "total": 1,
    }


def test_unauthorized(client, invalid_auth_headers):
    client.headers.update(invalid_auth_headers)
    assert client.post("/api/v1/menu/categories").status_code == 403
    assert client.patch("/api/v1/menu/categories/1").status_code == 403
    assert client.get("/api/v1/menu/categories/1").status_code == 403
    assert client.get("/api/v1/menu/categories").status_code == 403
    assert client.post("/api/v1/menu").status_code == 403
    assert client.patch("/api/v1/menu/1").status_code == 403
    assert client.get("/api/v1/menu/1").status_code == 403
    assert client.get("/api/v1/menu").status_code == 403
