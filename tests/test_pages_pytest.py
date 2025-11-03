"""Smoke tests for the HTML pages served by the application."""

import pytest


@pytest.mark.parametrize(
    ("path", "marker"),
    [
        ("/", "Sistema Galáctico de Usuarios"),
        ("/register", "Registrar usuario"),
        ("/login", "Login (solo demo)"),
        ("/users", "Usuarios"),
    ],
)
def test_pages_render(client, path, marker):
    response = client.get(path)
    assert response.status_code == 200
    assert b"<nav" in response.data.lower()
    assert marker.encode("utf-8") in response.data
