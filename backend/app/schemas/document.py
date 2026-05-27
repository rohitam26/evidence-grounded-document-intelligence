from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ChunkSchema(BaseModel):
    id: str
    document_id: str
    document_name: str
    page_number: int
    chunk_index: int
    section_heading: Optional[str] = ""
    content: str
    source_type: str
    content_hash: str
    embedding_model: str
    created_at: Optional[datetime] = None

class DocumentBase(BaseModel):
    filename: str
    file_type: str
    file_size_bytes: int

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    content_hash: str
    page_count: int
    processing_status: str
    processing_error: Optional[str] = None
    processing_duration_sec: float
    metadata_json: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

class DocumentDetailResponse(DocumentResponse):
    chunks: List[ChunkSchema] = []

class DocumentListResponse(BaseModel):
    total: int
    items: List[DocumentResponse]
