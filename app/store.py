"""In-memory storage for user records."""

from __future__ import annotations

from typing import Any, Dict

USERS: Dict[int, Dict[str, Any]] = {}
NEXT_ID: int = 1


def reset_store() -> None:
    """Reset the in-memory store (used mainly in tests)."""

    global USERS, NEXT_ID
    USERS = {}
    NEXT_ID = 1


__all__ = ["USERS", "NEXT_ID", "reset_store"]
