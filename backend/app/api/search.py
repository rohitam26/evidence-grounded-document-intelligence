from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.api.auth import require_auth
from app.schemas.search import SearchRequest
from app.services.search_service import search_service

search_bp = Blueprint("search", __name__)

@search_bp.route("", methods=["POST"])
@require_auth
def search():
    try:
        body = SearchRequest(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422

    res = search_service.search(
        query=body.query,
        document_ids=body.document_ids,
        top_k=body.top_k,
        mode=body.mode,
        rerank=body.rerank
    )
    return jsonify(res.model_dump())
