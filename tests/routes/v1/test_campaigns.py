from datetime import datetime, timezone

import freezegun


def test_campaigns(client, auth_headers):
    client.headers.update(auth_headers)
    # create
    payload = {
        "name": "Open Porch",
        "description": "Weekend open invitation",
        "date_start": "2021-12-18",
        "date_end": "2021-12-18",
    }
    date_created = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_created):
        response = client.post("/api/v1/campaigns", json=payload)
    assert response.status_code == 201
    campaign = response.json()
    assert campaign == {
        **payload,
        "id": 1,
        "date_created": date_created.isoformat(),
        "date_modified": date_created.isoformat(),
    }

    # edit
    payload = {**payload, "date_end": "2021-12-19"}
    date_modified = datetime.now(timezone.utc)
    with freezegun.freeze_time(date_modified):
        response = client.patch("/api/v1/campaigns/1", json=payload)
    assert response.status_code == 200
    campaign = response.json()
    assert campaign == {
        **payload,
        "id": 1,
        "date_created": date_created.isoformat(),
        "date_modified": date_modified.isoformat(),
    }

    # get one
    response = client.get("/api/v1/campaigns/1")
    assert response.status_code == 200
    assert response.json() == campaign

    # get many
    response = client.get("/api/v1/campaigns?offset=0&limit=10")
    assert response.status_code == 200
    assert response.json() == {
        "items": [campaign],
        "limit": 10,
        "offset": 0,
        "total": 1,
    }


def test_unauthorized(client, invalid_auth_headers):
    client.headers.update(invalid_auth_headers)
    assert client.post("/api/v1/campaigns").status_code == 403
    assert client.patch("/api/v1/campaigns/1").status_code == 403
    assert client.get("/api/v1/campaigns/1").status_code == 403
    assert client.get("/api/v1/campaigns?offset=0&limit=10").status_code == 403
