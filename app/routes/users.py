from __future__ import annotations

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from ..schemas import user_create_schema, user_update_schema
from ..store import create_user, delete_user, get_user, list_users, update_user

users_bp = Blueprint("users_api", __name__, url_prefix="/api/users")


@users_bp.post("")
def create_user_route():
    payload = request.get_json(silent=True) or {}
    try:
        data = user_create_schema.load(payload)
        user = create_user(data["name"], data["email"], data["password"])
        return jsonify(user), 201
    except ValidationError as ve:
        return jsonify({"error": "validation_error", "details": ve.messages}), 400
    except ValueError as ve:
        if str(ve) == "email_already_exists":
            return jsonify({"error": "email_already_exists"}), 409
        raise


@users_bp.get("")
def list_users_route():
    return jsonify(list_users()), 200


@users_bp.get("/<int:uid>")
def get_user_route(uid: int):
    user = get_user(uid)
    return (jsonify({"error": "not_found"}), 404) if not user else (jsonify(user), 200)


@users_bp.put("/<int:uid>")
def update_user_route(uid: int):
    payload = request.get_json(silent=True) or {}
    try:
        data = user_update_schema.load(payload)
        user = update_user(uid, **data)
        return (jsonify({"error": "not_found"}), 404) if not user else (jsonify(user), 200)
    except ValidationError as ve:
        return jsonify({"error": "validation_error", "details": ve.messages}), 400
    except ValueError as ve:
        if str(ve) == "email_already_exists":
            return jsonify({"error": "email_already_exists"}), 409
        raise


@users_bp.delete("/<int:uid>")
def delete_user_route(uid: int):
    return ("", 204) if delete_user(uid) else (jsonify({"error": "not_found"}), 404)
