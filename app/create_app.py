"""Application factory used by the service entry points."""

from __future__ import annotations

from flask import Flask, jsonify

from .config import get_config
from .store import reset_store


def register_error_handlers(app: Flask) -> None:
    """Register global error handlers with *app*."""

    @app.errorhandler(404)
    def handle_not_found(error):  # pragma: no cover - simple delegation
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):  # pragma: no cover - simple delegation
        return jsonify({"error": "Method not allowed."}), 405

    @app.errorhandler(500)
    def handle_server_error(error):  # pragma: no cover - simple delegation
        return jsonify({"error": "Internal server error."}), 500


def create_app(testing: bool = False) -> Flask:
    """Create and configure a :class:`~flask.Flask` application instance."""

    app = Flask(
        __name__, template_folder="templates", static_folder="static"
    )

    config_name = "test" if testing else None
    app.config.from_object(get_config(config_name))
    app.config["TESTING"] = testing

    if testing:
        reset_store()

    from .pages import pages_bp
    from .routes.users import users_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(users_bp)

    register_error_handlers(app)

    if testing:

        @app.post("/api/_debug/reset")
        def debug_reset():
            reset_store()
            return "", 204

    return app
