
from app.tests.conftest import USER


def test_get_all_users(client, insert_user_data):
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": USER["email"],
            "password": USER["password"],
        },
    )

    cookie = {"access_token": login_response.cookies.get("access_token")}

    response = client.get("/api/v1/users", cookies=cookie)
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 0
    assert response_data[0]["email"] == USER["email"]


def test_get_user(client, insert_user_data):
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": USER["email"],
            "password": USER["password"],
        },
    )

    cookie = {"access_token": login_response.cookies.get("access_token")}

    response = client.get("/api/v1/users/1", cookies=cookie)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    user_get_response = USER.copy()
    user_get_response.pop("password", None)
    user_get_response.update(
        {
            "role_id": 1,
            "avatar": None,
            "id": 1,
            "is_active": True,
            "is_email_verified": False,
            "avatar_url": None,
        }
    )
    assert response_data == user_get_response


def test_delete(client, insert_user_data):
    data = {"full_name": "Mr. A", "email": "test@mail.com", "password": "secret"}
    user = client.post("/api/v1/auth/register", data=data)

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": USER["email"], "password": USER["password"]},
    )

    cookie = {"access_token": login_response.cookies.get("access_token")}

    response = client.delete(f"/api/v1/users/{user.json()['id']}", cookies=cookie)

    assert response.status_code == 200


def test_activate_deactivate_user(client, insert_user_data):
    data = {"full_name": "Mr. A", "email": "test@mail.com", "password": "secret"}
    user = client.post("/api/v1/auth/register", data=data)

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": USER["email"], "password": USER["password"]},
    )

    cookie = {"access_token": login_response.cookies.get("access_token")}

    response = client.put(f"/api/v1/users/{user.json()['id']}/activate", cookies=cookie)
    assert response.status_code == 200
    response = client.get(f"/api/v1/users/{user.json()['id']}", cookies=cookie)
    assert response.json()["is_active"] is True

    response = client.put(
        f"/api/v1/users/{user.json()['id']}/deactivate", cookies=cookie
    )
    assert response.status_code == 200
    response = client.get(f"/api/v1/users/{user.json()['id']}", cookies=cookie)
    assert response.json()["is_active"] is False
