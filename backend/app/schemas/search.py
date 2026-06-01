from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query")
    document_ids: Optional[List[str]] = Field(default=None, description="Filter by document IDs")
    top_k: int = Field(default=5, ge=1, le=25, description="Number of results to return")
    mode: str = Field(default="hybrid", description="dense, sparse, or hybrid")
    rerank: bool = Field(default=True, description="Apply cross-encoder reranking")

class SearchResultItem(BaseModel):
    chunk_id: str
    document_id: str
    document_name: str
    page_number: int
    section_heading: Optional[str] = ""
    content: str
    score: float
    retrieval_method: str  # dense, sparse, hybrid_rrf, reranked
    metadata: Dict[str, Any] = {}

class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[SearchResultItem]
    retrieval_latency_ms: float
