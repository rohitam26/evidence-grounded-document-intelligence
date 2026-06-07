import os
import uuid
import time
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from app.config import settings
from app.core.database import init_db
from app.core.logging import logger
from app.api import api_bp

def create_app() -> Flask:
    """Application factory for PaperTrail REST API."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = settings.MAX_UPLOAD_SIZE_BYTES

    # CORS configuration
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Middleware: Request ID and structured request logging
    @app.before_request
    def before_request():
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        latency_ms = (time.time() - getattr(g, "start_time", time.time())) * 1000.0
        response.headers["X-Request-ID"] = getattr(g, "request_id", "")
        response.headers["X-Response-Time-Ms"] = f"{latency_ms:.2f}"
        if request.path not in ["/api/v1/health"]:
            logger.info(
                f"{request.method} {request.path} {response.status_code} - {latency_ms:.1f}ms",
                extra={"extra_fields": {"request_id": g.request_id, "status": response.status_code}}
            )
        return response

    # Centralized Error Handlers
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request", "details": str(e)}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(413)
    def payload_too_large(e):
        return jsonify({"error": "File size exceeds the 25MB maximum limit"}), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        logger.error(f"Internal server error: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

    # Register API Blueprints
    app.register_blueprint(api_bp)

    # Health shortcuts at root
    @app.route("/health")
    def root_health():
        return jsonify({"status": "healthy", "service": settings.PROJECT_NAME})

    @app.route("/")
    def index():
        return jsonify({
            "service": settings.PROJECT_NAME,
            "subtitle": settings.PROJECT_SUBTITLE,
            "version": settings.VERSION,
            "api_docs": f"{settings.API_V1_PREFIX}/docs/openapi.json"
        })

    # Initialize DB schema
    with app.app_context():
        init_db()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=settings.DEBUG)
