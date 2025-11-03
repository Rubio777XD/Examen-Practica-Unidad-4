from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..store import authenticate_user

auth_bp = Blueprint("auth_api", __name__, url_prefix="/api/auth")


@auth_bp.post("/login")
def login_route():
    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip()
    password = payload.get("password") or ""

    if not email or not password:
        return jsonify({"error": "validation_error"}), 400

    user = authenticate_user(email, password)
    if not user:
        return jsonify({"error": "invalid_credentials"}), 401

    return jsonify(user), 200
