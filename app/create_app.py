from __future__ import annotations

from flask import Flask, jsonify

from .config import get_config
from .store import reset_store


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    config_name = "test" if testing else None
    app.config.from_object(get_config(config_name))
    app.config.update(TESTING=testing)

    from .routes import auth_bp, users_bp, wall_bp
    from .pages import pages_bp

    if testing:
        reset_store()

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(wall_bp)
    app.register_blueprint(pages_bp)

    @app.get("/api/health")
    def health():  # pragma: no cover - trivial
        return {"status": "ok"}, 200

    @app.errorhandler(404)
    def handle_404(error):  # pragma: no cover - simple
        return jsonify({"error": "not_found"}), 404

    @app.errorhandler(405)
    def handle_405(error):  # pragma: no cover - simple
        return jsonify({"error": "method_not_allowed"}), 405

    @app.errorhandler(500)
    def handle_500(error):  # pragma: no cover - logging side effect
        app.logger.exception("Unhandled server error")
        return jsonify({"error": "internal_error"}), 500

    return app
