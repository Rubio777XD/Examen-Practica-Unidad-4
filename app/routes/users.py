"""Blueprint providing the CRUD endpoints for users stored in memory."""

from __future__ import annotations

from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, Iterable, List

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash

from .. import store
from ..schemas import user_create_schema, user_schema, user_update_schema, users_schema

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


def error_response(
    message: str, status: HTTPStatus, details: Dict[str, Any] | None = None
):
    payload: Dict[str, Any] = {"error": message}
    if details:
        payload["details"] = details
    return jsonify(payload), status


def sanitise_user(user: Dict[str, Any]) -> Dict[str, Any]:
    """Return *user* without internal fields such as ``password_hash``."""

    public_user = {key: value for key, value in user.items() if key != "password_hash"}
    return public_user


def sanitise_many(users: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [sanitise_user(user) for user in users]


def email_exists(email: str, *, exclude_id: int | None = None) -> bool:
    for uid, stored in store.USERS.items():
        if exclude_id is not None and uid == exclude_id:
            continue
        if stored["email"].lower() == email.lower():
            return True
    return False


@users_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    try:
        payload = user_create_schema.load(data)
    except ValidationError as err:
        return error_response("Invalid payload.", HTTPStatus.BAD_REQUEST, err.messages)

    if email_exists(payload["email"]):
        return error_response("Email already exists.", HTTPStatus.CONFLICT)

    uid = store.NEXT_ID
    store.NEXT_ID += 1
    store.USERS[uid] = {
        "id": uid,
        "name": payload["name"],
        "email": payload["email"],
        "password_hash": generate_password_hash(payload["password"]),
        "created_at": datetime.utcnow().isoformat(),
    }

    return (
        jsonify(user_schema.dump(sanitise_user(store.USERS[uid]))),
        HTTPStatus.CREATED,
    )


@users_bp.route("", methods=["GET"])
def list_users():
    users = [store.USERS[uid] for uid in sorted(store.USERS.keys())]

    page_raw = request.args.get("page")
    per_page_raw = request.args.get("per_page")

    if page_raw is not None or per_page_raw is not None:
        try:
            page = int(page_raw) if page_raw is not None else 1
            per_page = int(per_page_raw) if per_page_raw is not None else 10
        except ValueError:
            return error_response(
                "Pagination parameters must be integers.", HTTPStatus.BAD_REQUEST
            )

        if page < 1 or per_page < 1:
            return error_response(
                "Pagination parameters must be greater than zero.",
                HTTPStatus.BAD_REQUEST,
            )

        start = (page - 1) * per_page
        end = start + per_page
        users = users[start:end]

    return jsonify(users_schema.dump(sanitise_many(users))), HTTPStatus.OK


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    user = store.USERS.get(user_id)
    if not user:
        return error_response("User not found.", HTTPStatus.NOT_FOUND)
    return jsonify(user_schema.dump(sanitise_user(user))), HTTPStatus.OK


@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    user = store.USERS.get(user_id)
    if not user:
        return error_response("User not found.", HTTPStatus.NOT_FOUND)

    data = request.get_json(silent=True) or {}
    try:
        payload = user_update_schema.load(data)
    except ValidationError as err:
        return error_response("Invalid payload.", HTTPStatus.BAD_REQUEST, err.messages)

    if not payload:
        return error_response("No valid fields provided.", HTTPStatus.BAD_REQUEST)

    if "email" in payload and email_exists(payload["email"], exclude_id=user_id):
        return error_response("Email already exists.", HTTPStatus.CONFLICT)

    if "name" in payload:
        user["name"] = payload["name"]
    if "email" in payload:
        user["email"] = payload["email"]
    if "password" in payload:
        user["password_hash"] = generate_password_hash(payload["password"])

    return jsonify(user_schema.dump(sanitise_user(user))), HTTPStatus.OK


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    user = store.USERS.get(user_id)
    if not user:
        return error_response("User not found.", HTTPStatus.NOT_FOUND)

    store.USERS.pop(user_id)

    return "", HTTPStatus.NO_CONTENT
