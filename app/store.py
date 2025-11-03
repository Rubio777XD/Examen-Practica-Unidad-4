from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from werkzeug.security import generate_password_hash

USERS: Dict[int, Dict[str, Any]] = {}
NEXT_ID: int = 1


def reset_store() -> None:
    global USERS, NEXT_ID
    USERS = {}
    NEXT_ID = 1


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


__all__ = [
    "create_user",
    "delete_user",
    "get_user",
    "list_users",
    "reset_store",
    "update_user",
    "USERS",
    "NEXT_ID",
]
