from unittest.mock import MagicMock, patch

import pytest
from fastapi import Cookie
from freezegun import freeze_time

from app.tests.conftest import TASK, USER, insert_user_data


# @patch('app.models.base_model.datetime')
def test_create_task(client, insert_user_data):
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": USER["email"],
            "password": USER["password"],
        },
    )

    cookie = {"access_token": login_response.cookies.get("access_token")}
    response = client.post("/api/v1/tasks", cookies=cookie, json=TASK)
    assert response.status_code == 200
    response_data = response.json()
    response_data.pop("created_at", None)
    response_data.pop("updated_at", None)
    assert response_data == {
        "description": "Finish the report",
        "title": "Demo task title",
        "user_id": 1,
        "category": "Work",
        "status": False,
        "due_date": "2024-05-23T00:00:00",
        "id": 1,
        "priority_level": "LOW",
        "completed_at": None,
    }


@pytest.mark.skip(reason="pagination not working on test")
def test_get_all_tasks(client, insert_user_data):
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": USER["email"],
            "password": USER["password"],
        },
    )

    cookie = {"access_token": login_response.cookies.get("access_token")}
    response = client.get(
        "/api/v1/tasks", params={"page": 1, "size": 10}, cookies=cookie
    )

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert "items" in response_data


def test_get_task_by_id(client, insert_user_data):
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": USER["email"],
            "password": USER["password"],
        },
    )

    cookie = {"access_token": login_response.cookies.get("access_token")}
    client.post("/api/v1/tasks", cookies=cookie, json=TASK)

    response = client.get("/api/v1/tasks/1", cookies=cookie)

    assert response.status_code == 200
    response_data = response.json()
    response_data.pop("created_at", None)
    response_data.pop("updated_at", None)
    assert response_data == {
        "id": 1,
        "user_id": 1,
        "title": "Demo task title",
        "description": "Finish the report",
        "category": "Work",
        "status": False,
        "due_date": "2024-05-23T00:00:00",
        "task_state": "incomplete",
        "priority_level": "LOW",
        "completed_at": None,
    }


def test_update_task(client, insert_user_data):
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": USER["email"],
            "password": USER["password"],
        },
    )

    cookie = {"access_token": login_response.cookies.get("access_token")}
    client.post("/api/v1/tasks", cookies=cookie, json=TASK)

    update_data = {
        "title": "Updated Task Title",
        "description": "Updated description",
        "category": "Updated",
        "priority_level": "LOW",
        "due_date": "2024-05-24T00:00:00",
    }

    response = client.put("/api/v1/tasks/1", json=update_data, cookies=cookie)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == update_data["title"]
    assert response_data["description"] == update_data["description"]
    response_data = response.json()
    response_data.pop("created_at", None)
    response_data.pop("updated_at", None)
    update_data.update(
        {
            "id": 1,
            "user_id": 1,
            "status": False,
            "task_state": "incomplete",
            "completed_at": None,
        }
    )

    assert response_data == update_data


def test_mark_as_complete(client, insert_user_data):
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": USER["email"],
            "password": USER["password"],
        },
    )

    cookie = {"access_token": login_response.cookies.get("access_token")}
    client.post("/api/v1/tasks", cookies=cookie, json=TASK)

    response = client.put("/api/v1/tasks/1/complete", cookies=cookie)

    assert response.status_code == 200
    assert response.json()["status"] is True
    assert response.json()["completed_at"] is not None


def test_mark_as_incomplete(client, insert_user_data):
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": USER["email"],
            "password": USER["password"],
        },
    )

    cookie = {"access_token": login_response.cookies.get("access_token")}
    client.post("/api/v1/tasks", cookies=cookie, json=TASK)

    response = client.put("/api/v1/tasks/1/incomplete", cookies=cookie)

    assert response.status_code == 200
    assert response.json()["status"] is False
    assert response.json()["completed_at"] is None


def test_delete_task(client, insert_user_data):
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": USER["email"], "password": USER["password"]},
    )

    cookie = {"access_token": login_response.cookies.get("access_token")}
    client.post("/api/v1/tasks", cookies=cookie, json=TASK)

    response = client.delete("/api/v1/tasks/1", cookies=cookie)

    assert response.status_code == 200
