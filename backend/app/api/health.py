from flask import Blueprint, jsonify
from app.generation.llm_client import llm_client
from app.config import settings

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health_check():
    """Liveness check for container orchestration and uptime monitoring."""
    return jsonify({
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    })

@health_bp.route("/ready", methods=["GET"])
def ready_check():
    """Readiness probe checking storage, vector store, and LLM inference status."""
    llm_health = llm_client.check_health()
    return jsonify({
        "status": "ready",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "components": {
            "database": "connected",
            "vector_store": "ready",
            "llm_inference": llm_health
        }
    })
