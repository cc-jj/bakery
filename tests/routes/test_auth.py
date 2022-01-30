from src import auth


def test_login(client, user):
    response = client.post(
        "/auth/token", json={"username": "cj", "password": "hunter123"}
    )
    assert response.status_code == 200
    token = response.json()["token"]
    username = auth.decode_username(token)
    assert username == "cj"

    response = client.post(
        "/auth/token", json={"username": "doesnt exist", "password": "hunter123"}
    )
    assert response.status_code == 400

    response = client.post(
        "/auth/token", json={"username": "cj", "password": "wrong-password"}
    )
    assert response.status_code == 400
