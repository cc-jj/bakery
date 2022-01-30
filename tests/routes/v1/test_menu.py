from datetime import datetime, timezone

import freezegun


def test_categories(client, auth_headers):
    client.headers.update(auth_headers)

    # create
    payload = {
        "name": "Cocoa Bomb",
    }
    date_created = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_created):
        response = client.post("/v1/menu/categories/", json=payload)
    assert response.status_code == 201
    category = response.json()
    assert category == {
        **payload,
        "id": 1,
        "date_created": date_created.isoformat(),
        "date_modified": date_created.isoformat(),
    }

    # edit
    payload = {**payload, "id": 1, "name": "Cocoa Bombs"}
    date_modified = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_modified):
        response = client.patch("/v1/menu/categories/", json=payload)
    assert response.status_code == 200
    category = response.json()
    assert category == {
        **payload,
        "date_created": date_created.isoformat(),
        "date_modified": date_modified.isoformat(),
    }

    # get one
    response = client.get("/v1/menu/categories/1")
    assert response.status_code == 200
    assert response.json() == category

    # get many
    response = client.get("/v1/menu/categories/?offset=0&limit=10")
    assert response.status_code == 200
    assert response.json() == {
        "items": [category],
        "limit": 10,
        "offset": 0,
        "total": 1,
    }


def test_menu_items(client, auth_headers, menu_category):
    client.headers.update(auth_headers)

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
        response = client.post("/v1/menu/", json=payload)
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
    payload = {**payload, "id": 1, "price": 6.0}
    date_modified = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_modified):
        response = client.patch("/v1/menu/", json=payload)
    assert response.status_code == 200
    menu_item = response.json()
    assert menu_item == {
        **payload,
        "category": menu_category,
        "date_created": date_created.isoformat(),
        "date_modified": date_modified.isoformat(),
    }

    # get one
    response = client.get("/v1/menu/1")
    assert response.status_code == 200
    assert response.json() == menu_item

    # get many
    response = client.get("/v1/menu/?offset=0&limit=10")
    assert response.status_code == 200
    assert response.json() == {
        "items": [menu_item],
        "limit": 10,
        "offset": 0,
        "total": 1,
    }


def test_unauthorized(client, invalid_auth_headers):
    client.headers.update(invalid_auth_headers)
    assert client.post("/v1/menu/categories/").status_code == 403
    assert client.patch("/v1/menu/categories/").status_code == 403
    assert client.get("/v1/menu/categories/1").status_code == 403
    assert client.get("/v1/menu/categories/").status_code == 403
    assert client.post("/v1/menu/").status_code == 403
    assert client.patch("/v1/menu/").status_code == 403
    assert client.get("/v1/menu/1").status_code == 403
    assert client.get("/v1/menu/").status_code == 403
