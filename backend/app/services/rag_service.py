import time
from typing import List, Optional, Dict, Any
from app.retrieval.hybrid import hybrid_search_engine
from app.generation.grounder import grounded_rag_engine
from app.schemas.search import SearchResponse, SearchResultItem
from app.schemas.chat import ChatResponse
from app.core.database import get_db_session
from app.models import Document, Chunk

class SearchService:
    """Search service coordinator."""

    def search(
        self,
        query: str,
        document_ids: Optional[List[str]] = None,
        top_k: int = 5,
        mode: str = "hybrid",
        rerank: bool = True
    ) -> SearchResponse:
        start_time = time.time()
        results = hybrid_search_engine.search(
            query=query,
            top_k=top_k,
            document_ids=document_ids,
            mode=mode,
            apply_rerank=rerank
        )
        latency = (time.time() - start_time) * 1000.0

        items = [
            SearchResultItem(
                chunk_id=r["chunk_id"],
                document_id=r["document_id"],
                document_name=r["document_name"],
                page_number=r["page_number"],
                section_heading=r.get("section_heading", ""),
                content=r["content"],
                score=r["score"],
                retrieval_method=r["retrieval_method"],
                metadata=r.get("metadata", {})
            )
            for r in results
        ]

        return SearchResponse(
            query=query,
            total_results=len(items),
            results=items,
            retrieval_latency_ms=round(latency, 2)
        )

class RAGService:
    """Grounded RAG conversational assistant service."""

    def answer_query(
        self,
        message: str,
        document_ids: Optional[List[str]] = None,
        top_k: int = 5,
        strict_grounding: bool = True
    ) -> ChatResponse:
        retrieved_chunks = hybrid_search_engine.search(
            query=message,
            top_k=top_k,
            document_ids=document_ids,
            mode="hybrid",
            apply_rerank=True
        )

        return grounded_rag_engine.generate_grounded_answer(
            question=message,
            retrieved_chunks=retrieved_chunks,
            strict_grounding=strict_grounding
        )

search_service = SearchService()
rag_service = RAGService()
