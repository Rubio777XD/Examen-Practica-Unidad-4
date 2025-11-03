"""Marshmallow schemas for serialising and validating payloads."""

from __future__ import annotations

from marshmallow import Schema, fields, post_load, validates

from .validators import validate_name, validate_password


class UserSchema(Schema):
    """Schema used for serialising user dictionaries."""

    id = fields.Int(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.Str(required=True)


class UserCreateSchema(Schema):
    """Schema used for validating user creation payloads."""

    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

    @validates("name")
    def _validate_name(self, value: str) -> None:
        validate_name(value)

    @validates("password")
    def _validate_password(self, value: str) -> None:
        validate_password(value)


class UserUpdateSchema(Schema):
    """Schema used for validating user update payloads."""

    name = fields.Str(required=False)
    email = fields.Email(required=False)
    password = fields.Str(required=False, load_only=True)

    @validates("name")
    def _validate_name(self, value: str) -> None:
        validate_name(value)

    @validates("password")
    def _validate_password(self, value: str) -> None:
        validate_password(value)

    @post_load
    def remove_empty(self, data: dict, **_: object) -> dict:
        """Remove keys whose value is ``None``."""

        return {key: value for key, value in data.items() if value is not None}


user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_create_schema = UserCreateSchema()
user_update_schema = UserUpdateSchema()


__all__ = [
    "UserSchema",
    "UserCreateSchema",
    "UserUpdateSchema",
    "user_schema",
    "users_schema",
    "user_create_schema",
    "user_update_schema",
]
