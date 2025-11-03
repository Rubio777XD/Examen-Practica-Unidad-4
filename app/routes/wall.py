from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..store import create_post, list_posts

wall_bp = Blueprint("wall_api", __name__, url_prefix="/api/wall")


@wall_bp.get("/posts")
def list_posts_route():
    return jsonify(list_posts()), 200


@wall_bp.post("/posts")
def create_post_route():
    payload = request.get_json(silent=True) or {}
    content = payload.get("content")
    author = request.headers.get("X-Author")

    try:
        post = create_post(content, author)
    except ValueError as exc:
        if str(exc) == "invalid_content":
            return jsonify({"error": "invalid_content"}), 400
        raise

    return jsonify(post), 201
