from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    report_type: str
    content_markdown: str
    evidence_citations: List[Dict[str, Any]] = []
    created_at: datetime
