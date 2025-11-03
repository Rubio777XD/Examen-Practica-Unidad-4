from __future__ import annotations

from marshmallow import Schema, fields, post_load, validates

from .validators import validate_name, validate_password


class UserSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.Str(required=True, dump_only=True)


class UserCreateSchema(Schema):
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
