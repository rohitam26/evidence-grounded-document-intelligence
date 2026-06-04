from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class StepTrace(BaseModel):
    step_number: int
    action: str
    tool_name: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    tool_output: Optional[Any] = None
    timestamp: str

class AgentRunRequest(BaseModel):
    goal: str = Field(..., min_length=3, description="Goal for the autonomous analysis agent")
    document_ids: Optional[List[str]] = None

class AgentRunResponse(BaseModel):
    run_id: str
    goal: str
    status: str  # pending, running, completed, failed
    steps: List[StepTrace] = []
    final_output: Optional[str] = None
    duration_sec: float = 0.0
    created_at: Optional[datetime] = None
