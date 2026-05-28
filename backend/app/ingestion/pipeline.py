import os
import time
import uuid
from typing import Dict, Any, Optional
from app.config import settings
from app.core.logging import logger
from app.utils.hashing import compute_file_hash
from app.core.database import get_db_session
from app.models import Document, Chunk
from app.ingestion.parser import document_parser
from app.ingestion.chunker import chunker
from app.retrieval.embeddings import embedding_generator
from app.retrieval.vector_store import vector_store
from app.retrieval.bm25 import bm25_retriever

class IngestionPipeline:
    """Document Ingestion Pipeline handling validation, parsing, chunking, embedding, and indexing."""

    def process_file(
        self,
        file_path: str,
        filename: str,
        user_id: str,
        existing_doc_id: Optional[str] = None
    ) -> Dict[str, Any]:
        start_time = time.time()
        file_size = os.path.getsize(file_path)
        content_hash = compute_file_hash(file_path)
        ext = os.path.splitext(filename)[1].lower()

        doc_id = existing_doc_id or str(uuid.uuid4())

        with get_db_session() as db:
            doc = db.query(Document).filter(Document.id == doc_id).first()
            if not doc:
                # Check for duplicate document
                duplicate = db.query(Document).filter(
                    Document.content_hash == content_hash,
                    Document.user_id == user_id
                ).first()
                if duplicate:
                    logger.info(f"Duplicate document detected for hash {content_hash} (Existing: {duplicate.id})")
                    return {
                        "document_id": duplicate.id,
                        "status": "duplicate",
                        "message": f"Document already exists as '{duplicate.filename}'"
                    }

                doc = Document(
                    id=doc_id,
                    user_id=user_id,
                    filename=filename,
                    stored_path=file_path,
                    file_type=ext,
                    file_size_bytes=file_size,
                    content_hash=content_hash,
                    processing_status="processing"
                )
                db.add(doc)
            else:
                doc.processing_status = "processing"
                doc.processing_error = None
                # Clear existing chunks if reprocessing
                db.query(Chunk).filter(Chunk.document_id == doc_id).delete()
                vector_store.delete_document_chunks(doc_id)
                bm25_retriever.remove_document(doc_id)

        try:
            # 1. Parse document blocks
            parsed_blocks = document_parser.parse(file_path, ext)
            page_numbers = {b.page_number for b in parsed_blocks}
            page_count = max(page_numbers) if page_numbers else 1

            # 2. Structure-aware chunking
            doc_chunks = chunker.chunk_document(
                blocks=parsed_blocks,
                document_id=doc_id,
                document_name=filename
            )

            # 3. Generate embeddings
            chunk_texts = [c.content for c in doc_chunks]
            embeddings = embedding_generator.embed_texts(chunk_texts)

            # 4. Index in Vector Store and BM25
            chunk_dicts = [c.to_dict() for c in doc_chunks]
            vector_store.upsert_chunks(chunk_dicts, embeddings)
            bm25_retriever.add_chunks(chunk_dicts)

            duration = time.time() - start_time

            # 5. Persist chunks in Database
            with get_db_session() as db:
                doc = db.query(Document).filter(Document.id == doc_id).first()
                if doc:
                    doc.page_count = page_count
                    doc.processing_status = "completed"
                    doc.processing_duration_sec = round(duration, 3)
                    doc.metadata_json = {
                        "chunk_count": len(doc_chunks),
                        "page_count": page_count,
                        "source_types": list({c.source_type for c in doc_chunks})
                    }

                    for c in doc_chunks:
                        db_chunk = Chunk(
                            id=c.chunk_id,
                            document_id=c.document_id,
                            document_name=c.document_name,
                            page_number=c.page_number,
                            chunk_index=c.chunk_index,
                            section_heading=c.section_heading,
                            content=c.content,
                            source_type=c.source_type,
                            content_hash=c.content_hash,
                            embedding_model=c.embedding_model,
                            qdrant_point_id=c.chunk_id
                        )
                        db.add(db_chunk)

            logger.info(f"Document {filename} ({doc_id}) successfully processed: {len(doc_chunks)} chunks, {duration:.2f}s")
            return {
                "document_id": doc_id,
                "status": "completed",
                "chunks_count": len(doc_chunks),
                "page_count": page_count,
                "duration_sec": round(duration, 3)
            }

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Failed to process document {filename}: {e}", exc_info=True)
            with get_db_session() as db:
                doc = db.query(Document).filter(Document.id == doc_id).first()
                if doc:
                    doc.processing_status = "failed"
                    doc.processing_error = str(e)
                    doc.processing_duration_sec = round(duration, 3)
            return {
                "document_id": doc_id,
                "status": "failed",
                "error": str(e),
                "duration_sec": round(duration, 3)
            }

ingestion_pipeline = IngestionPipeline()
