from app.tests.conftest import USER


def test_create_user(client):
    data = {"full_name": "Mr. A", "email": "demo@mail.com", "password": "secret"}

    response = client.post("/api/v1/auth/register", data=data)

    assert response.status_code == 200
    assert "password" not in response.json()


def test_login(client, insert_user_data):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": USER["email"],
            "password": USER["password"],
            "grant_type": None,
            "scope": None,
            "client_id": None,
            "client_secret": None,
        },
    )

    assert response.status_code == 200
    assert response.cookies.get("access_token") is not None
    assert response.cookies.get("refresh_token") is not None


def test_refresh_token(client, insert_user_data):
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": USER["email"],
            "password": USER["password"],
            "grant_type": None,
            "scope": None,
            "client_id": None,
            "client_secret": None,
        },
    )

    client.cookies.set("refresh_token", login_response.cookies.get("refresh_token"))

    response = client.post("/api/v1/auth/refresh_token")

    assert response.status_code == 200
    assert response.cookies.get("access_token") is not None
    assert response.cookies.get("refresh_token") is None


def test_logout(client, insert_user_data):
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": USER["email"],
            "password": USER["password"],
            "grant_type": None,
            "scope": None,
            "client_id": None,
            "client_secret": None,
        },
    )
    client.cookies.set("access_token", login_response.cookies.get("access_token"))

    response = client.get("/api/v1/auth/logout")
    assert response.status_code == 200
