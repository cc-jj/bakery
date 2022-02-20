from src import auth


def test_login_logout(client):
    response = client.post("/api/auth/login", json={"username": "cj", "password": "hunter123"})
    assert response.status_code == 200
    token = response.cookies.get("token")
    assert token is not None
    session = auth.decode_token(token)
    assert session["username"] == "cj"

    response = client.get("/api/auth/logout")
    assert response.status_code == 204
    assert response.cookies.get("token") is None

    response = client.post(
        "/api/auth/login", json={"username": "doesnt exist", "password": "hunter123"}
    )
    assert response.status_code == 400

    response = client.post("/api/auth/login", json={"username": "cj", "password": "wrong-password"})
    assert response.status_code == 400
