from __future__ import annotations

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.create_app import create_app


@pytest.fixture()
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()
