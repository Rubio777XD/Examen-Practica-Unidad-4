"""Shared pytest fixtures for the test suite."""

from __future__ import annotations

import pytest
from werkzeug.security import generate_password_hash

from app.create_app import create_app
from app.extensions import db
from app.models import User


@pytest.fixture()
def app():
    app = create_app("test")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def session(app):
    return db.session


@pytest.fixture()
def user_factory(session):
    def factory(**overrides):
        data = {
            "name": "Test User",
            "email": overrides.get("email", "user@example.com"),
            "password_hash": generate_password_hash("password123"),
        }
        data.update(overrides)
        user = User(**data)
        session.add(user)
        session.commit()
        return user

    return factory
