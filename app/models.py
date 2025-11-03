"""Database models for the application."""

from __future__ import annotations

from sqlalchemy import func

from .extensions import db


class User(db.Model):
    """User entity stored in the database."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def __repr__(self) -> str:  # pragma: no cover - representation helper
        return f"<User {self.email}>"


__all__ = ["User"]
