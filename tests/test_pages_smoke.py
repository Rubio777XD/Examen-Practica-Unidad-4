from __future__ import annotations


def test_pages_ok(client):
    for path in ("/", "/register", "/login", "/users"):
        assert client.get(path).status_code == 200
