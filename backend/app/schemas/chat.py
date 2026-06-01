from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Citation(BaseModel):
    citation_id: int
    document_id: str
    document_name: str
    page_number: int
    source_passage: str
    relevance_score: float
    evidence_status: str = "verified"  # verified, indirect, unverified

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    document_ids: Optional[List[str]] = None
    top_k: int = Field(default=5, ge=1, le=10)
    strict_grounding: bool = Field(default=True)

class ChatResponse(BaseModel):
    answer: str
    abstained: bool = False
    abstention_reason: Optional[str] = None
    citations: List[Citation] = []
    grounding_confidence: float = 0.0
    latency_ms: float = 0.0
