from __future__ import annotations


def test_create_user_success(client):
    payload = {"name": "Alice", "email": "alice@example.com", "password": "Secret123"}
    response = client.post("/api/users", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "password_hash" not in data


def test_create_user_duplicate_email(client):
    payload = {"name": "Alice", "email": "alice@example.com", "password": "Secret123"}
    first = client.post("/api/users", json=payload)
    assert first.status_code == 201

    second = client.post("/api/users", json=payload)

    assert second.status_code == 409
    assert second.get_json()["error"] == "email_already_exists"


def test_list_users(client):
    client.post("/api/users", json={"name": "Alice", "email": "alice@example.com", "password": "Secret123"})
    client.post("/api/users", json={"name": "Bob", "email": "bob@example.com", "password": "Secret123"})

    response = client.get("/api/users")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    emails = {user["email"] for user in data}
    assert emails == {"alice@example.com", "bob@example.com"}
