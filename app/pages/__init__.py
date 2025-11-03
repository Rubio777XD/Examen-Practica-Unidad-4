"""Blueprint exposing HTML pages for the web frontend."""

from flask import Blueprint

pages_bp = Blueprint(
    "pages",
    __name__,
    template_folder="../templates",
)

from . import views  # noqa: E402,F401  ensure views are registered
