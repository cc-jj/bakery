from datetime import datetime, timezone

import freezegun

from src import models


def test_order_items(client, auth_headers, order):
    client.headers.update(auth_headers)
    # create
    payload = {
        "order_id": order["id"],
        "menu_item_id": order["order_items"][0]["menu_item_id"],
        "menu_price": 50,
        "quantity": 10,
        "charged_price": 50,
        "notes": "Addon",
    }
    date_created = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_created):
        response = client.post("/v1/orders/items/", json=payload)
    assert response.status_code == 201
    order_with_new_item = response.json()
    original_order_item = order["order_items"][0]
    new_order_item = {
        **payload,
        "menu_item": original_order_item["menu_item"],
        "id": 2,
        "date_created": date_created.isoformat(),
        "date_modified": date_created.isoformat(),
    }
    assert order_with_new_item == {
        **order,
        "order_items": [
            original_order_item,
            new_order_item,
        ],
    }

    # edit
    payload = {**payload, "id": 2, "charged_price": 55}
    date_modified = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_modified):
        response = client.patch("/v1/orders/items/", json=payload)
    assert response.status_code == 200
    order_with_new_item = response.json()
    new_order_item = {
        **new_order_item,
        **payload,
        "date_modified": date_modified.isoformat(),
    }
    assert order_with_new_item == {
        **order,
        "order_items": [
            original_order_item,
            new_order_item,
        ],
    }

    # delete
    response = client.delete("/v1/orders/items/2")
    assert response.status_code == 200
    assert response.json() == order


def test_orders(client, auth_headers, campaign, customer, menu_item, db):
    client.headers.update(auth_headers)
    # create
    payload = {
        "customer_id": customer["id"],
        "campaign_id": campaign["id"],
        "date_ordered": "2021-12-20",
        "date_delivered": "2021-12-23",
        "price_adjustment": 20.0,
        "notes": "$20 delivery fee",
        "completed": True,
        "order_items": [
            {
                "menu_item_id": menu_item["id"],
                "quantity": 5,
                "menu_price": 5 * menu_item["price"],
                "charged_price": 5 * menu_item["price"],
                "notes": "a note",
            }
        ],
        "payments": [
            {
                "amount": 5 * menu_item["price"],
                "method": "cash",
                "date": "2021-12-23",
            }
        ],
    }
    date_created = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_created):
        response = client.post("/v1/orders/", json=payload)
    assert response.status_code == 201
    order = response.json()
    assert order == {
        **payload,
        "id": 1,
        "date_created": date_created.isoformat(),
        "date_modified": date_created.isoformat(),
        "customer": customer,
        "campaign": campaign,
        "order_items": [
            {
                **payload["order_items"][0],
                "id": 1,
                "order_id": 1,
                "menu_item": menu_item,
                "date_created": date_created.isoformat(),
                "date_modified": date_created.isoformat(),
            }
        ],
        "payments": [
            {
                **payload["payments"][0],
                "id": 1,
                "order_id": 1,
                "date_created": date_created.isoformat(),
                "date_modified": date_created.isoformat(),
            }
        ],
    }

    # edit
    payload = {**payload, "id": 1, "price_adjustment": 25, "notes": "$25 delivery fee"}
    payload.pop("order_items")
    payload.pop("payments")
    date_modified = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_modified):
        response = client.patch("/v1/orders/", json=payload)
    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order == {
        **order,
        **payload,
        "date_modified": date_modified.isoformat(),
    }

    # get one
    response = client.get("/v1/orders/1")
    assert response.status_code == 200
    assert response.json() == updated_order

    # get many
    response = client.get("/v1/orders/?completed=True")
    assert response.status_code == 200
    assert response.json() == {
        "items": [updated_order],
        "offset": 0,
        "limit": 50,
        "total": 1,
    }

    response = client.get("/v1/orders/?completed=False")
    assert response.status_code == 200
    assert response.json() == {"items": [], "offset": 0, "limit": 50, "total": 0}

    # delete
    response = client.delete("/v1/orders/1")
    assert response.status_code == 200
    assert response.json() == {"success": True}

    # associated payments / items should also be deleted
    assert db.query(models.Order).count() == 0
    assert db.query(models.Payment).count() == 0
    assert db.query(models.OrderItem).count() == 0


def test_unauthorized(client, invalid_auth_headers):
    client.headers.update(invalid_auth_headers)
    assert client.post("/v1/orders/").status_code == 403
    assert client.patch("/v1/orders/").status_code == 403
    assert client.get("/v1/orders/1").status_code == 403
    assert client.get("/v1/orders/").status_code == 403
    assert client.delete("/v1/orders/1").status_code == 403
    assert client.post("/v1/orders/items/").status_code == 403
    assert client.patch("/v1/orders/items/").status_code == 403
    assert client.delete("/v1/orders/items/1").status_code == 403
