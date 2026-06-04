from typing import List, Dict, Any, Optional, TypedDict
from datetime import datetime

class AgentState(TypedDict):
    run_id: str
    user_id: str
    goal: str
    document_ids: Optional[List[str]]
    intent: Optional[str]
    plan_steps: List[str]
    current_step_index: int
    retrieved_evidence: List[Dict[str, Any]]
    extracted_data: Dict[str, Any]
    comparison_results: Optional[Dict[str, Any]]
    validated_citations: List[Dict[str, Any]]
    report_markdown: Optional[str]
    execution_trace: List[Dict[str, Any]]
    status: str
    error: Optional[str]
