"""Functional tests for the user API using pytest."""

from __future__ import annotations

from werkzeug.security import check_password_hash

from app.models import User


def test_create_user_success(client, session):
    payload = {"name": "Alice", "email": "alice@example.com", "password": "secret123"}
    response = client.post("/api/users", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "password_hash" not in data
    assert User.query.filter_by(email=payload["email"]).one()


def test_create_user_invalid_email(client):
    payload = {"name": "Bob", "email": "invalid-email", "password": "secret123"}
    response = client.post("/api/users", json=payload)

    assert response.status_code == 400
    body = response.get_json()
    assert body["error"] == "Invalid payload."
    assert "email" in body["details"]


def test_create_user_duplicate_email(client, user_factory):
    user_factory(email="carol@example.com")
    payload = {"name": "Carol", "email": "carol@example.com", "password": "secret123"}

    response = client.post("/api/users", json=payload)

    assert response.status_code == 409
    body = response.get_json()
    assert body["error"] == "Email already exists."


def test_create_user_short_password(client):
    payload = {"name": "Dave", "email": "dave@example.com", "password": "short"}
    response = client.post("/api/users", json=payload)

    assert response.status_code == 400
    body = response.get_json()
    assert "password" in body["details"]


def test_list_users_pagination(client, user_factory):
    for index in range(15):
        user_factory(email=f"user{index}@example.com")

    response = client.get("/api/users", query_string={"page": 2, "per_page": 5})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["pagination"]["page"] == 2
    assert payload["pagination"]["per_page"] == 5
    assert len(payload["items"]) == 5


def test_list_users_invalid_pagination(client):
    response = client.get("/api/users", query_string={"page": "abc"})

    assert response.status_code == 400
    assert response.get_json()["error"] == "Pagination parameters must be integers."


def test_get_user_success(client, user_factory):
    user = user_factory(email="eve@example.com")

    response = client.get(f"/api/users/{user.id}")

    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == user.email
    assert "password_hash" not in data


def test_get_user_not_found(client):
    response = client.get("/api/users/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found."


def test_update_user_success(client, user_factory):
    user = user_factory(email="frank@example.com")

    response = client.put(
        f"/api/users/{user.id}",
        json={"name": "Frank Updated", "email": "frank.updated@example.com"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Frank Updated"
    assert data["email"] == "frank.updated@example.com"


def test_update_user_with_password(client, user_factory, session):
    user = user_factory(email="grace@example.com")
    previous_hash = user.password_hash

    response = client.put(
        f"/api/users/{user.id}",
        json={"password": "newpass123"},
    )

    assert response.status_code == 200
    session.refresh(user)
    assert not check_password_hash(previous_hash, "newpass123")
    assert check_password_hash(user.password_hash, "newpass123")


def test_update_user_validation_error(client, user_factory):
    user = user_factory(email="harry@example.com")

    response = client.put(
        f"/api/users/{user.id}",
        json={"email": "not-an-email"},
    )

    assert response.status_code == 400
    assert "email" in response.get_json()["details"]


def test_update_user_duplicate_email(client, user_factory):
    user_factory(email="ingrid@example.com")
    user = user_factory(email="isaac@example.com")

    response = client.put(
        f"/api/users/{user.id}",
        json={"email": "ingrid@example.com"},
    )

    assert response.status_code == 409
    assert response.get_json()["error"] == "Email already exists."


def test_update_user_not_found(client):
    response = client.put("/api/users/999", json={"name": "Ghost"})

    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found."


def test_delete_user_success(client, user_factory, session):
    user = user_factory(email="jack@example.com")

    response = client.delete(f"/api/users/{user.id}")

    assert response.status_code == 204
    assert session.get(User, user.id) is None


def test_delete_user_not_found(client):
    response = client.delete("/api/users/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found."
