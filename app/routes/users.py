"""Blueprint providing the CRUD endpoints for :class:`~app.models.User`."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash

from ..extensions import db
from ..models import User
from ..schemas import user_create_schema, user_schema, user_update_schema, users_schema

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


def error_response(
    message: str, status: HTTPStatus, details: Dict[str, Any] | None = None
):
    payload: Dict[str, Any] = {"error": message}
    if details:
        payload["details"] = details
    return jsonify(payload), status


def paginate_query(
    query, page: int, per_page: int
) -> Tuple[list[User], Dict[str, int]]:
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
    }


@users_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    try:
        payload = user_create_schema.load(data)
    except ValidationError as err:
        return error_response("Invalid payload.", HTTPStatus.BAD_REQUEST, err.messages)

    existing = User.query.filter_by(email=payload["email"]).first()
    if existing:
        return error_response("Email already exists.", HTTPStatus.CONFLICT)

    user = User(
        name=payload["name"],
        email=payload["email"],
        password_hash=generate_password_hash(payload["password"]),
    )
    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user)), HTTPStatus.CREATED


@users_bp.route("", methods=["GET"])
def list_users():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        return error_response(
            "Pagination parameters must be integers.", HTTPStatus.BAD_REQUEST
        )

    page = max(page, 1)
    per_page = min(max(per_page, 1), 100)

    users, pagination = paginate_query(User.query.order_by(User.id), page, per_page)
    return (
        jsonify({"items": users_schema.dump(users), "pagination": pagination}),
        HTTPStatus.OK,
    )


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return error_response("User not found.", HTTPStatus.NOT_FOUND)
    return jsonify(user_schema.dump(user)), HTTPStatus.OK


@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return error_response("User not found.", HTTPStatus.NOT_FOUND)

    data = request.get_json(silent=True) or {}
    try:
        payload = user_update_schema.load(data)
    except ValidationError as err:
        return error_response("Invalid payload.", HTTPStatus.BAD_REQUEST, err.messages)

    if not payload:
        return error_response("No valid fields provided.", HTTPStatus.BAD_REQUEST)

    if "email" in payload:
        existing = User.query.filter(
            User.email == payload["email"], User.id != user.id
        ).first()
        if existing:
            return error_response("Email already exists.", HTTPStatus.CONFLICT)

    if "name" in payload:
        user.name = payload["name"]
    if "email" in payload:
        user.email = payload["email"]
    if "password" in payload:
        user.password_hash = generate_password_hash(payload["password"])

    db.session.commit()

    return jsonify(user_schema.dump(user)), HTTPStatus.OK


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return error_response("User not found.", HTTPStatus.NOT_FOUND)

    db.session.delete(user)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT
