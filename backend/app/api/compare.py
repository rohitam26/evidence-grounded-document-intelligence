from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from app.api.auth import require_auth
from app.schemas.comparison import ComparisonRequest
from app.services.comparison_service import comparison_service

compare_bp = Blueprint("compare", __name__)

@compare_bp.route("", methods=["POST"])
@require_auth
def compare():
    try:
        body = ComparisonRequest(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422

    try:
        res = comparison_service.compare(
            document_a_id=body.document_a_id,
            document_b_id=body.document_b_id,
            user_id=g.user_id,
            category=body.category
        )
        return jsonify(res.model_dump())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
