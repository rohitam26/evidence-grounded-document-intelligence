from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class DiffItem(BaseModel):
    category: str
    attribute_name: str
    value_a: Optional[str] = None
    value_b: Optional[str] = None
    difference_summary: str
    evidence_a: str
    page_a: int
    evidence_b: str
    page_b: int
    is_conflict: bool
    verification_status: str = "verified"

class ComparisonRequest(BaseModel):
    document_a_id: str
    document_b_id: str
    category: str = Field(default="payment_terms", description="payment_terms, dates, obligations, or all")

class ComparisonResponse(BaseModel):
    comparison_id: str
    document_a_id: str
    document_b_id: str
    document_a_name: str
    document_b_name: str
    category: str
    differences: List[DiffItem]
    conflict_count: int
