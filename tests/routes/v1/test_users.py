def test_me(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "cj"}

    client.get("/api/auth/logout")
    response = client.get("/api/v1/users/me")
    assert response.status_code == 403
