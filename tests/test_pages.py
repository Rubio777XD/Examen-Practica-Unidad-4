from __future__ import annotations


import pytest


@pytest.mark.parametrize("path", ["/", "/login", "/register", "/users", "/muro"])
def test_pages_render(client, path):
    response = client.get(path)

    assert response.status_code == 200
    assert b"<!doctype html>" in response.data
