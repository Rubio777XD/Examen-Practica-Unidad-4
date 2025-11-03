from __future__ import annotations


def test_get_posts_initial_state(client):
    response = client.get("/api/wall/posts")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_post_with_author_header(client):
    response = client.post(
        "/api/wall/posts",
        json={"content": "Hola mundo"},
        headers={"X-Author": "Alice"},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["author"] == "Alice"
    assert data["content"] == "Hola mundo"


def test_create_post_without_author(client):
    response = client.post(
        "/api/wall/posts",
        json={"content": "Mensaje anónimo"},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["author"] == "Anónimo"
    assert data["content"] == "Mensaje anónimo"


def test_create_post_empty_content(client):
    response = client.post(
        "/api/wall/posts",
        json={"content": "   "},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "invalid_content"
