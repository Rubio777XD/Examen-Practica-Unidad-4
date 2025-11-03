"""Application factory used by the service entry points."""

from __future__ import annotations

from flask import Flask, jsonify

from .config import get_config
from .extensions import db, ma, migrate


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


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure a :class:`~flask.Flask` application instance."""

    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from .pages import pages_bp
    from .routes.users import users_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(users_bp)

    register_error_handlers(app)

    @app.shell_context_processor
    def make_shell_context():  # pragma: no cover - developer convenience
        from .models import User

        return {"db": db, "User": User}

    return app
