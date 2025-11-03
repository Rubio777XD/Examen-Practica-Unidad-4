from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from werkzeug.security import check_password_hash, generate_password_hash

USERS: Dict[int, Dict[str, Any]] = {}
NEXT_ID: int = 1
POSTS: List[Dict[str, Any]] = []
NEXT_POST_ID: int = 1


def reset_store() -> None:
    global USERS, NEXT_ID, POSTS, NEXT_POST_ID
    USERS = {}
    NEXT_ID = 1
    POSTS = []
    NEXT_POST_ID = 1


def _public_user(user: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in user.items() if k != "password_hash"}


def create_user(name: str, email: str, password: str) -> Dict[str, Any]:
    global NEXT_ID, USERS
    for existing in USERS.values():
        if existing["email"].lower() == email.lower():
            raise ValueError("email_already_exists")
    uid = NEXT_ID
    NEXT_ID += 1
    user = {
        "id": uid,
        "name": name,
        "email": email,
        "password_hash": generate_password_hash(password),
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    USERS[uid] = user
    return _public_user(user)


def list_users() -> list[Dict[str, Any]]:
    return [_public_user(user) for user in USERS.values()]


def get_user(uid: int):
    user = USERS.get(uid)
    return None if not user else _public_user(user)


def _find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    lowered = email.lower()
    for user in USERS.values():
        if user["email"].lower() == lowered:
            return user
    return None


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    user = _find_user_by_email(email)
    if not user:
        return None
    if not check_password_hash(user["password_hash"], password):
        return None
    return _public_user(user)


def update_user(
    uid: int,
    *,
    name: str | None = None,
    email: str | None = None,
    password: str | None = None,
):
    user = USERS.get(uid)
    if not user:
        return None
    if email and any(
        other["email"].lower() == email.lower() and other_id != uid
        for other_id, other in USERS.items()
    ):
        raise ValueError("email_already_exists")
    if name:
        user["name"] = name
    if email:
        user["email"] = email
    if password:
        user["password_hash"] = generate_password_hash(password)
    return _public_user(user)


def delete_user(uid: int) -> bool:
    return USERS.pop(uid, None) is not None


def create_post(content: str, author: Optional[str]) -> Dict[str, Any]:
    global NEXT_POST_ID, POSTS
    text = (content or "").strip()
    if not text:
        raise ValueError("invalid_content")
    if len(text) > 500:
        raise ValueError("invalid_content")
    post = {
        "id": NEXT_POST_ID,
        "author": (author or "").strip() or "Anónimo",
        "content": text,
        "created_at": datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
    }
    NEXT_POST_ID += 1
    POSTS.append(post)
    return post


def list_posts() -> List[Dict[str, Any]]:
    return list(reversed(POSTS))


__all__ = [
    "create_user",
    "delete_user",
    "get_user",
    "list_users",
    "reset_store",
    "update_user",
    "authenticate_user",
    "create_post",
    "list_posts",
    "USERS",
    "NEXT_ID",
    "POSTS",
    "NEXT_POST_ID",
]
