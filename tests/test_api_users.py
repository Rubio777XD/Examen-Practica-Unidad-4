from __future__ import annotations


def test_create_user_ok(client):
    rv = client.post(
        "/api/users",
        json={"name": "Ana", "email": "ana@test.com", "password": "secreto123"},
    )
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["name"] == "Ana"
    assert "id" in data and "password_hash" not in data


def test_email_unico(client):
    client.post(
        "/api/users",
        json={"name": "A", "email": "dup@test.com", "password": "secreto123"},
    )
    rv = client.post(
        "/api/users",
        json={"name": "B", "email": "dup@test.com", "password": "secreto123"},
    )
    assert rv.status_code in (400, 409)


def test_list_users(client):
    rv = client.get("/api/users")
    assert rv.status_code == 200
    assert isinstance(rv.get_json(), list)


def test_update_and_delete(client):
    u = client.post(
        "/api/users",
        json={"name": "Bob", "email": "bob@test.com", "password": "secreto123"},
    ).get_json()
    rv_up = client.put(f"/api/users/{u['id']}", json={"name": "Bob2"})
    assert rv_up.status_code == 200 and rv_up.get_json()["name"] == "Bob2"
    rv_del = client.delete(f"/api/users/{u['id']}")
    assert rv_del.status_code in (200, 204)
