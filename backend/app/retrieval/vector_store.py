import os
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from app.config import settings
from app.core.logging import logger

class VectorStore:
    """Vector store manager wrapping Qdrant with local/memory and server modes."""

    def __init__(self):
        self.collection_name = settings.QDRANT_COLLECTION
        self.dim = settings.EMBEDDING_DIM
        self.client = self._init_client()
        self._ensure_collection()

    def _init_client(self) -> QdrantClient:
        if settings.QDRANT_HOST:
            logger.info(f"Connecting to Qdrant server at {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
            return QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        elif settings.QDRANT_PATH:
            try:
                os.makedirs(settings.QDRANT_PATH, exist_ok=True)
                logger.info(f"Using local file-backed Qdrant store at {settings.QDRANT_PATH}")
                return QdrantClient(path=settings.QDRANT_PATH)
            except Exception as e:
                logger.warning(f"File-backed Qdrant locked or unavailable ({e}); falling back to memory mode.")
                return QdrantClient(":memory:")
        else:
            logger.info("Using in-memory Qdrant store")
            return QdrantClient(":memory:")

    def _ensure_collection(self):
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            if not exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qmodels.VectorParams(
                        size=self.dim,
                        distance=qmodels.Distance.COSINE
                    )
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error ensuring Qdrant collection: {e}")

    def upsert_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Upsert document chunks and vectors into Qdrant."""
        if not chunks:
            return

        points = []
        for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
            point_id = chunk.get("chunk_id")
            payload = {
                "chunk_id": point_id,
                "document_id": chunk.get("document_id"),
                "document_name": chunk.get("document_name"),
                "page_number": chunk.get("page_number"),
                "chunk_index": chunk.get("chunk_index"),
                "section_heading": chunk.get("section_heading", ""),
                "content": chunk.get("content"),
                "source_type": chunk.get("source_type"),
                "content_hash": chunk.get("content_hash")
            }
            points.append(qmodels.PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            ))

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        logger.info(f"Upserted {len(points)} chunks into Qdrant collection {self.collection_name}")

    def search_dense(
        self,
        query_vector: List[float],
        top_k: int = 5,
        document_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Search dense vectors with optional document filtering."""
        query_filter = None
        if document_ids:
            query_filter = qmodels.Filter(
                must=[
                    qmodels.FieldCondition(
                        key="document_id",
                        match=qmodels.MatchAny(any=document_ids)
                    )
                ]
            )

        try:
            # Compatible with latest qdrant-client search / query_points
            if hasattr(self.client, "search"):
                results = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    limit=top_k,
                    query_filter=query_filter
                )
                return [
                    {
                        "chunk_id": r.payload.get("chunk_id"),
                        "document_id": r.payload.get("document_id"),
                        "document_name": r.payload.get("document_name"),
                        "page_number": r.payload.get("page_number"),
                        "section_heading": r.payload.get("section_heading", ""),
                        "content": r.payload.get("content"),
                        "score": float(r.score),
                        "retrieval_method": "dense",
                        "metadata": r.payload
                    }
                    for r in results
                ]
            else:
                resp = self.client.query_points(
                    collection_name=self.collection_name,
                    query=query_vector,
                    limit=top_k,
                    query_filter=query_filter
                )
                return [
                    {
                        "chunk_id": p.payload.get("chunk_id"),
                        "document_id": p.payload.get("document_id"),
                        "document_name": p.payload.get("document_name"),
                        "page_number": p.payload.get("page_number"),
                        "section_heading": p.payload.get("section_heading", ""),
                        "content": p.payload.get("content"),
                        "score": float(p.score),
                        "retrieval_method": "dense",
                        "metadata": p.payload
                    }
                    for p in resp.points
                ]
        except Exception as e:
            logger.error(f"Dense vector search failed: {e}")
            return []

    def delete_document_chunks(self, document_id: str):
        """Remove all chunks associated with a document."""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=qmodels.FilterSelector(
                    filter=qmodels.Filter(
                        must=[
                            qmodels.FieldCondition(
                                key="document_id",
                                match=qmodels.MatchValue(value=document_id)
                            )
                        ]
                    )
                )
            )
            logger.info(f"Deleted chunks for document {document_id} from Qdrant")
        except Exception as e:
            logger.error(f"Error deleting chunks for document {document_id}: {e}")

vector_store = VectorStore()
