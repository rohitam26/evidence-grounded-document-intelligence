from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.api.auth import require_auth
from app.schemas.extraction import ExtractionRequest
from app.services.extraction_service import extraction_service

extract_bp = Blueprint("extract", __name__)

@extract_bp.route("", methods=["POST"])
@require_auth
def extract():
    try:
        body = ExtractionRequest(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422

    try:
        res = extraction_service.extract(document_id=body.document_id, schema_name=body.schema_name)
        return jsonify(res.model_dump())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
