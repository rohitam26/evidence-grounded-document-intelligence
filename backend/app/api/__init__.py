from flask import Blueprint, jsonify
from app.api.auth import auth_bp
from app.api.documents import documents_bp
from app.api.search import search_bp
from app.api.chat import chat_bp
from app.api.extract import extract_bp
from app.api.compare import compare_bp
from app.api.agent import agent_bp
from app.api.reports import reports_bp
from app.api.health import health_bp
from app.config import settings

api_bp = Blueprint("api_v1", __name__, url_prefix=settings.API_V1_PREFIX)

api_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_bp.register_blueprint(documents_bp, url_prefix="/documents")
api_bp.register_blueprint(search_bp, url_prefix="/search")
api_bp.register_blueprint(chat_bp, url_prefix="/chat")
api_bp.register_blueprint(extract_bp, url_prefix="/extract")
api_bp.register_blueprint(compare_bp, url_prefix="/compare")
api_bp.register_blueprint(agent_bp, url_prefix="/agent")
api_bp.register_blueprint(reports_bp, url_prefix="/reports")
api_bp.register_blueprint(health_bp, url_prefix="")

@api_bp.route("/docs", methods=["GET"])
def swagger_ui():
    """Interactive Swagger UI documentation."""
    return """<!DOCTYPE html>
<html>
<head>
    <title>Evidence-Grounded Document Intelligence - Swagger UI</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
</head>
<body style="margin: 0; background: #fafafa;">
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        window.ui = SwaggerUIBundle({
            url: '/api/v1/docs/openapi.json',
            dom_id: '#swagger-ui',
            deepLinking: true,
            presets: [SwaggerUIBundle.presets.apis]
        });
    </script>
</body>
</html>"""

@api_bp.route("/docs/openapi.json", methods=["GET"])
def get_openapi_spec():
    """OpenAPI 3.0 specification for PaperTrail API."""
    return jsonify({
        "openapi": "3.0.3",
        "info": {
            "title": settings.PROJECT_NAME,
            "description": settings.PROJECT_SUBTITLE,
            "version": settings.VERSION
        },
        "servers": [{"url": settings.API_V1_PREFIX}],
        "paths": {
            "/auth/login": {"post": {"summary": "User Login", "tags": ["Auth"]}},
            "/auth/register": {"post": {"summary": "User Registration", "tags": ["Auth"]}},
            "/documents/upload": {"post": {"summary": "Upload & Ingest Document", "tags": ["Documents"]}},
            "/documents": {"get": {"summary": "List Ingested Documents", "tags": ["Documents"]}},
            "/documents/{id}": {"get": {"summary": "Get Document Chunks & Metadata", "tags": ["Documents"]}},
            "/documents/{id}": {"delete": {"summary": "Delete Document & Vectors", "tags": ["Documents"]}},
            "/documents/{id}/reprocess": {"post": {"summary": "Reprocess Document", "tags": ["Documents"]}},
            "/search": {"post": {"summary": "Hybrid Evidence Search", "tags": ["Search"]}},
            "/chat": {"post": {"summary": "Evidence-Grounded RAG Chat", "tags": ["Chat"]}},
            "/extract": {"post": {"summary": "Structured Schema Extraction", "tags": ["Extraction"]}},
            "/compare": {"post": {"summary": "Multi-Document Difference Audit", "tags": ["Comparison"]}},
            "/agent/run": {"post": {"summary": "Execute Autonomous Document Agent", "tags": ["Agent"]}},
            "/agent/runs/{id}": {"get": {"summary": "Get Agent Run Execution Trace", "tags": ["Agent"]}},
            "/reports": {"get": {"summary": "List Audited Reports", "tags": ["Reports"]}},
            "/health": {"get": {"summary": "Liveness Check", "tags": ["System"]}},
            "/ready": {"get": {"summary": "Readiness Check", "tags": ["System"]}}
        }
    })
