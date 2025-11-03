"""Pure validation helpers used across the application."""

from __future__ import annotations

import re

from email_validator import EmailNotValidError, validate_email

NAME_REGEX = re.compile(r"^[\w\s\-']+$")


class ValidationError(ValueError):
    """Exception raised when validation fails."""


def is_valid_email(value: str) -> bool:
    """Return ``True`` if *value* is a syntactically valid email address."""

    try:
        validate_email(value)
    except EmailNotValidError as exc:  # pragma: no cover - defensive
        raise ValidationError(str(exc)) from exc
    return True


def validate_name(value: str) -> None:
    """Validate that *value* is a non-empty human readable name."""

    if value is None:
        raise ValidationError("Name is required.")
    if not isinstance(value, str) or not value.strip():
        raise ValidationError("Name must be a non-empty string.")
    if not 2 <= len(value.strip()) <= 80:
        raise ValidationError("Name must be between 2 and 80 characters long.")
    if not NAME_REGEX.match(value.strip()):
        raise ValidationError("Name contains invalid characters.")


def validate_password(value: str) -> None:
    """Validate that *value* meets password requirements."""

    if value is None:
        raise ValidationError("Password is required.")
    if not isinstance(value, str):
        raise ValidationError("Password must be a string.")
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.")


__all__ = [
    "ValidationError",
    "is_valid_email",
    "validate_name",
    "validate_password",
]
