from __future__ import annotations


def test_create_user_ok(client):
    rv = client.post(
        "/api/users",
        json={"name": "Ana", "email": "ana@test.com", "password": "secreto123"},
    )
    assert rv.status_code == 201
    data = rv.get_json()
    assert data == {
        "id": data["id"],
        "name": "Ana",
        "email": "ana@test.com",
        "created_at": data["created_at"],
    }


def test_create_user_duplicate_email_conflict(client):
    client.post(
        "/api/users",
        json={"name": "Ana", "email": "dup@test.com", "password": "secreto123"},
    )
    rv = client.post(
        "/api/users",
        json={"name": "Ben", "email": "dup@test.com", "password": "secreto123"},
    )
    assert rv.status_code == 409
    assert rv.get_json() == {"error": "email_already_exists"}


def test_list_users_returns_users(client):
    client.post(
        "/api/users",
        json={"name": "Ana", "email": "ana@test.com", "password": "secreto123"},
    )
    rv = client.get("/api/users")
    assert rv.status_code == 200
    body = rv.get_json()
    assert isinstance(body, list)
    assert body and {"id", "name", "email", "created_at"}.issubset(body[0].keys())


def test_get_user_not_found(client):
    rv = client.get("/api/users/999")
    assert rv.status_code == 404
    assert rv.get_json() == {"error": "not_found"}


def test_update_user_success(client):
    created = client.post(
        "/api/users",
        json={"name": "Ana", "email": "ana@test.com", "password": "secreto123"},
    ).get_json()
    rv = client.put(
        f"/api/users/{created['id']}",
        json={"name": "Ana María", "email": "ana2@test.com"},
    )
    assert rv.status_code == 200
    assert rv.get_json()["email"] == "ana2@test.com"


def test_delete_user_success(client):
    created = client.post(
        "/api/users",
        json={"name": "Ana", "email": "ana@test.com", "password": "secreto123"},
    ).get_json()
    rv = client.delete(f"/api/users/{created['id']}")
    assert rv.status_code == 204
    rv_follow = client.get(f"/api/users/{created['id']}")
    assert rv_follow.status_code == 404
