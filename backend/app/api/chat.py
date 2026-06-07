from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.api.auth import require_auth
from app.schemas.chat import ChatRequest
from app.services.rag_service import rag_service

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("", methods=["POST"])
@require_auth
def chat():
    try:
        body = ChatRequest(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422

    res = rag_service.answer_query(
        message=body.message,
        document_ids=body.document_ids,
        top_k=body.top_k,
        strict_grounding=body.strict_grounding
    )
    return jsonify(res.model_dump())
