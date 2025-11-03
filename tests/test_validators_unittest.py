"""Unit tests for validator helper functions using unittest."""

from __future__ import annotations

import unittest

from app.validators import (
    ValidationError,
    is_valid_email,
    validate_name,
    validate_password,
)


class EmailValidatorTests(unittest.TestCase):
    def test_valid_email(self):
        self.assertTrue(is_valid_email("user@example.com"))

    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            is_valid_email("invalid")


class NameValidatorTests(unittest.TestCase):
    def test_valid_name(self):
        validate_name("Valid Name")

    def test_blank_name(self):
        with self.assertRaises(ValidationError):
            validate_name(" ")

    def test_short_name(self):
        with self.assertRaises(ValidationError):
            validate_name("A")

    def test_long_name(self):
        with self.assertRaises(ValidationError):
            validate_name("A" * 81)

    def test_invalid_characters(self):
        with self.assertRaises(ValidationError):
            validate_name("Invalid@Name")


class PasswordValidatorTests(unittest.TestCase):
    def test_valid_password(self):
        validate_password("strongpass")

    def test_short_password(self):
        with self.assertRaises(ValidationError):
            validate_password("short")

    def test_missing_password(self):
        with self.assertRaises(ValidationError):
            validate_password(None)  # type: ignore[arg-type]


if __name__ == "__main__":  # pragma: no cover - unittest entry-point
    unittest.main()
