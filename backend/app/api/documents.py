import os
import shutil
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, g
from app.api.auth import require_auth
from app.config import settings
from app.core.database import get_db_session
from app.models import Document, Chunk
from app.ingestion.pipeline import ingestion_pipeline
from app.retrieval.vector_store import vector_store
from app.retrieval.bm25 import bm25_retriever
from app.schemas.document import DocumentResponse, DocumentDetailResponse, ChunkSchema

documents_bp = Blueprint("documents", __name__)

@documents_bp.route("/upload", methods=["POST"])
@require_auth
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        return jsonify({
            "error": f"File extension '{ext}' not allowed. Permitted: {settings.ALLOWED_EXTENSIONS}"
        }), 400

    filename = secure_filename(file.filename)
    dest_path = os.path.join(settings.STORAGE_DIR, filename)
    file.save(dest_path)

    res = ingestion_pipeline.process_file(
        file_path=dest_path,
        filename=filename,
        user_id=g.user_id
    )

    return jsonify(res), 201 if res["status"] == "completed" else 200

@documents_bp.route("", methods=["GET"])
@require_auth
def list_documents():
    with get_db_session() as db:
        docs = db.query(Document).order_by(Document.created_at.desc()).all()
        items = []
        for d in docs:
            items.append({
                "id": d.id,
                "filename": d.filename,
                "file_type": d.file_type,
                "file_size_bytes": d.file_size_bytes,
                "content_hash": d.content_hash,
                "page_count": d.page_count,
                "processing_status": d.processing_status,
                "processing_error": d.processing_error,
                "processing_duration_sec": d.processing_duration_sec,
                "metadata_json": d.metadata_json,
                "created_at": d.created_at.isoformat() if d.created_at else None,
                "updated_at": d.updated_at.isoformat() if d.updated_at else None
            })
    return jsonify({"total": len(items), "items": items})

@documents_bp.route("/<document_id>", methods=["GET"])
@require_auth
def get_document(document_id: str):
    with get_db_session() as db:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return jsonify({"error": "Document not found"}), 404
        chunks = db.query(Chunk).filter(Chunk.document_id == document_id).order_by(Chunk.chunk_index).all()
        chunk_items = [
            {
                "id": c.id,
                "document_id": c.document_id,
                "document_name": c.document_name,
                "page_number": c.page_number,
                "chunk_index": c.chunk_index,
                "section_heading": c.section_heading,
                "content": c.content,
                "source_type": c.source_type,
                "content_hash": c.content_hash,
                "embedding_model": c.embedding_model,
                "created_at": c.created_at.isoformat() if c.created_at else None
            }
            for c in chunks
        ]
        return jsonify({
            "id": doc.id,
            "filename": doc.filename,
            "file_type": doc.file_type,
            "file_size_bytes": doc.file_size_bytes,
            "content_hash": doc.content_hash,
            "page_count": doc.page_count,
            "processing_status": doc.processing_status,
            "processing_error": doc.processing_error,
            "processing_duration_sec": doc.processing_duration_sec,
            "metadata_json": doc.metadata_json,
            "chunks": chunk_items,
            "created_at": doc.created_at.isoformat() if doc.created_at else None
        })

@documents_bp.route("/<document_id>", methods=["DELETE"])
@require_auth
def delete_document(document_id: str):
    with get_db_session() as db:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return jsonify({"error": "Document not found"}), 404

        # Remove from vector store and BM25
        vector_store.delete_document_chunks(document_id)
        bm25_retriever.remove_document(document_id)

        # Remove file from disk
        if os.path.exists(doc.stored_path):
            try:
                os.remove(doc.stored_path)
            except Exception:
                pass

        db.delete(doc)

    return jsonify({"message": f"Document {document_id} deleted successfully"})

@documents_bp.route("/<document_id>/reprocess", methods=["POST"])
@require_auth
def reprocess_document(document_id: str):
    with get_db_session() as db:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return jsonify({"error": "Document not found"}), 404
        path = doc.stored_path
        filename = doc.filename

    res = ingestion_pipeline.process_file(
        file_path=path,
        filename=filename,
        user_id=g.user_id,
        existing_doc_id=document_id
    )
    return jsonify(res)
