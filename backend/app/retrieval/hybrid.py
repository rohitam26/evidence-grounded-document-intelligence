from typing import List, Dict, Any, Optional
from app.config import settings
from app.retrieval.embeddings import embedding_generator
from app.retrieval.vector_store import vector_store
from app.retrieval.bm25 import bm25_retriever
from app.retrieval.reranker import reranker
from app.core.logging import logger

class HybridSearchEngine:
    """Hybrid search combining Dense vector retrieval and Sparse BM25 via Reciprocal Rank Fusion (RRF)."""

    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k

    def search(
        self,
        query: str,
        top_k: int = settings.RETRIEVAL_TOP_K,
        document_ids: Optional[List[str]] = None,
        mode: str = "hybrid",
        apply_rerank: bool = True
    ) -> List[Dict[str, Any]]:
        """Execute search in dense, sparse, or hybrid RRF mode with optional reranking."""
        candidate_k = top_k * 3 if apply_rerank else top_k

        if mode == "dense":
            query_vec = embedding_generator.embed_query(query)
            results = vector_store.search_dense(query_vec, top_k=candidate_k, document_ids=document_ids)
        elif mode == "sparse":
            results = bm25_retriever.search_sparse(query, top_k=candidate_k, document_ids=document_ids)
        else:
            # Hybrid RRF
            query_vec = embedding_generator.embed_query(query)
            dense_results = vector_store.search_dense(query_vec, top_k=candidate_k, document_ids=document_ids)
            sparse_results = bm25_retriever.search_sparse(query, top_k=candidate_k, document_ids=document_ids)

            results = self._reciprocal_rank_fusion(
                dense_results=dense_results,
                sparse_results=sparse_results,
                top_k=candidate_k
            )

        if apply_rerank and results:
            results = reranker.rerank(query=query, candidate_chunks=results, top_k=top_k)
        else:
            results = results[:top_k]

        return results

    def _reciprocal_rank_fusion(
        self,
        dense_results: List[Dict[str, Any]],
        sparse_results: List[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Reciprocal Rank Fusion (RRF) algorithm."""
        rrf_scores: Dict[str, float] = {}
        chunks_by_id: Dict[str, Dict[str, Any]] = {}

        dense_weight = settings.DENSE_WEIGHT
        sparse_weight = settings.SPARSE_WEIGHT

        for rank, item in enumerate(dense_results):
            cid = item["chunk_id"]
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (dense_weight / (self.rrf_k + rank + 1))
            chunks_by_id[cid] = item

        for rank, item in enumerate(sparse_results):
            cid = item["chunk_id"]
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (sparse_weight / (self.rrf_k + rank + 1))
            if cid not in chunks_by_id:
                chunks_by_id[cid] = item

        fused = []
        for cid, score in rrf_scores.items():
            chunk = dict(chunks_by_id[cid])
            chunk["score"] = round(score, 6)
            chunk["retrieval_method"] = "hybrid_rrf"
            fused.append(chunk)

        fused.sort(key=lambda x: x["score"], reverse=True)
        return fused[:top_k]

hybrid_search_engine = HybridSearchEngine()
