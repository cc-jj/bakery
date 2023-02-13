from datetime import datetime, timezone

import freezegun


def test_campaigns(client):
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


def test_create_campaign_unique_constraint(client, campaign):
    payload = {"name": campaign["name"], "description": "foo"}
    response = client.post("/api/v1/campaigns", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "A campaign already exists with that name"}


def test_edit_campaign_unique_constraint(client, campaign):
    campaign_2 = {"name": "foo", "description": "bar"}
    response = client.post("/api/v1/campaigns", json=campaign_2)
    assert response.status_code == 201

    updates = campaign
    del updates["date_created"]
    del updates["date_modified"]
    campaign_id = updates.pop("id")
    updates["name"] = "foo"

    response = client.patch(f"/api/v1/campaigns/{campaign_id}", json=updates)
    assert response.status_code == 400
    assert response.json() == {"detail": "A campaign already exists with that name"}


def test_unauthorized(client):
    client.get("/api/auth/logout")
    assert client.post("/api/v1/campaigns").status_code == 403
    assert client.patch("/api/v1/campaigns/1").status_code == 403
    assert client.get("/api/v1/campaigns/1").status_code == 403
    assert client.get("/api/v1/campaigns?offset=0&limit=10").status_code == 403
