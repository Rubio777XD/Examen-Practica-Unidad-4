from __future__ import annotations

import pytest


def create_user(client, *, name="Test User", email="test@example.com", password="Secret123"):
    response = client.post(
        "/api/users",
        json={"name": name, "email": email, "password": password},
    )
    assert response.status_code == 201
    return response.get_json()


def test_login_success(client):
    user = create_user(client)

    response = client.post(
        "/api/auth/login",
        json={"email": user["email"], "password": "Secret123"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == user["id"]
    assert data["email"] == user["email"]
    assert "password_hash" not in data


@pytest.mark.parametrize(
    "email,password",
    [
        ("test@example.com", "WrongPass"),
        ("invalid@example.com", "Secret123"),
    ],
)
def test_login_invalid_credentials(client, email, password):
    create_user(client)

    response = client.post("/api/auth/login", json={"email": email, "password": password})

    assert response.status_code == 401
    assert response.get_json()["error"] == "invalid_credentials"


def test_login_missing_fields(client):
    response = client.post("/api/auth/login", json={"email": ""})

    assert response.status_code == 400
    assert response.get_json()["error"] == "validation_error"
