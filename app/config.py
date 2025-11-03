"""Configuration objects for the Flask application."""

from __future__ import annotations

import os


class Config:
    """Base configuration shared across environments."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Configuration for local development."""

    DEBUG = True


class TestingConfig(Config):
    """Configuration used during automated tests."""

    TESTING = True


class ProductionConfig(Config):
    """Configuration for production deployments."""

    DEBUG = False


CONFIG_MAP = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(name: str | None = None) -> type[Config]:
    """Return the configuration class associated with *name*.

    Parameters
    ----------
    name:
        Optional configuration name. When omitted, ``default`` is used.
    """

    if not name:
        name = "default"
    return CONFIG_MAP.get(name, DevelopmentConfig)
