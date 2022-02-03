from datetime import datetime, timezone

import freezegun


def test_payments(client, order):

    # create
    payload = {
        "order_id": order["id"],
        "amount": 10,
        "method": "zelle",
        "date": "2021-12-22",
    }
    date_created = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_created):
        response = client.post("/api/v1/payments", json=payload)
    assert response.status_code == 201
    order_with_payment = response.json()
    payment = {
        **payload,
        "id": 1,
        "date_created": date_created.isoformat(),
        "date_modified": date_created.isoformat(),
    }
    assert order_with_payment == {**order, "payments": [payment]}

    # edit
    payload = {**payload, "date": "2021-12-19"}
    date_modified = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_modified):
        response = client.patch("/api/v1/payments/1", json=payload)
    assert response.status_code == 200
    order_with_payment = response.json()
    payment = {
        **payment,
        **payload,
        "id": 1,
        "date_modified": date_modified.isoformat(),
    }
    assert order_with_payment == {**order, "payments": [payment]}

    # get many
    response = client.get("/api/v1/payments?offset=0&limit=10")
    assert response.status_code == 200
    assert response.json() == {
        "items": [payment],
        "limit": 10,
        "offset": 0,
        "total": 1,
    }

    # delete
    response = client.delete("/api/v1/payments/1")
    assert response.status_code == 200
    order_without_payment = response.json()
    assert order_without_payment == order


def test_unauthorized(client, invalid_auth_headers):
    client.headers.update(invalid_auth_headers)
    assert client.post("/api/v1/payments").status_code == 403
    assert client.patch("/api/v1/payments/1").status_code == 403
    assert client.get("/api/v1/payments").status_code == 403
    assert client.delete("/api/v1/payments/1").status_code == 403
